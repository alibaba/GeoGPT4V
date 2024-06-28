import os
import time
import argparse
import json
import jsonlines

from tqdm import tqdm
from PIL import Image
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from utils.data_process import read_jsonl, write_jsonl
from constant.rerank_prompt import gpt4v_system_prompt_description
from utils.gpt_api import gpt4v_api
from utils.regular_function import find_score
import multiprocessing

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--instruction_file', type=str)
    parser.add_argument('--output_file', type=str)
    parser.add_argument('--api_key', type=str)
    parser.add_argument('--gen_num', type=int, default=1)
    parser.add_argument('--model', type=str, default='gpt4v')
    parser.add_argument('--max_retry_num', type=int, default=5)
    parser.add_argument('--mp_num', type=int, default=1)
    return parser.parse_args()

def construct_prompt(data):
    image = data['image_description']
    prompt = f"Image description:{image}"
    return prompt

def build_k_data(data_list):
    res_dict = {}
    for data in data_list:
        if data['id'] not in res_dict:
            res_dict[data['id']] = []
        res_dict[data['id']].append(data)
    return res_dict

def rerank_gpt4v(data_list, args):
    start_time = time.time()
    score_list = []
    for data in data_list:
        user_prompt = construct_prompt(data)
        image_path = data['image_path']
        if not os.path.exists(image_path):
            score_list.append(-1.0)
            continue
        gpt4v_system_prompt = gpt4v_system_prompt_description
        response = gpt4v_api((gpt4v_system_prompt, user_prompt, image_path, args.api_key, args.gen_num, args.max_retry_num))

        score = find_score(response)
        score_list.append(float(score))
        time.sleep(3)

    if len(score_list) == 0:
        return None
    index = score_list.index(max(score_list))
    data = data_list[index]
    new_data = data.copy()
    new_data['score'] = score_list[index]
    end_time = time.time()
    print("requestion time = ", end_time - start_time)
    return (new_data, args)
        
def setcallback(x):
    if x is not None:
        new_data, args = x
        with open(args.output_file, "a", encoding='utf-8') as file:
            file.write(json.dumps(new_data, ensure_ascii=False))
            file.write('\n')

        
if __name__ == '__main__':
    args = get_args()
    # makedir
    output_dir = os.path.dirname(args.output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    #read file
    instruction_list = read_jsonl(args.instruction_file)
    full_id = [data['id'] for data in instruction_list]
    
    # remove finished id
    if os.path.exists(args.output_file):
        finish_list = read_jsonl(args.output_file)
        finish_id = [data['id'] for data in finish_list]
        unfinish_id = [id for id in full_id if id not in finish_id]
    else:
        unfinish_id = full_id
    
    unfinish_instruction_list = [data for data in instruction_list if data['id'] in unfinish_id]
    print("unfinish_instruction_list len = ", len(unfinish_instruction_list))
    data_dict = build_k_data(unfinish_instruction_list)
    pool = multiprocessing.Pool(args.mp_num)
    if args.model == 'gpt4v':
        for id, data_list in data_dict.items():
            pool.apply_async(func=rerank_gpt4v, args=(data_list, args), callback=setcallback)
        pool.close()
        pool.join()
    else:
        print("[Error]Unsupport model")
    
    