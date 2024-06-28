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
from utils.run_mathematica_code import run_code
from utils.gpt_api import gpt4_api
from utils.regular_function import find_code
from constant.gen_image_prompt import gpt4_geoqa_system_prompt
import multiprocessing

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--instruction_file', type=str)
    parser.add_argument('--output_file', type=str)
    parser.add_argument('--api_key', type=str)
    parser.add_argument('--gen_num', type=int, default=1)
    parser.add_argument('--dataset', type=str, default='geoqa')
    parser.add_argument('--max_retry_num', type=int, default=5)
    parser.add_argument('--code_dir', type=str)
    parser.add_argument('--image_dir', type=str)
    parser.add_argument('--mp_num', type=int, default=1)
    return parser.parse_args()

def construct_choice(choice_list):
    num2label = ['A', "B", "C", "D"]
    choice_str = ""
    for idx, choice in enumerate(choice_list):
        choice_str += f"\n{num2label[idx]}. {choice}"
    return choice_str

def construct_prompt(data, args):
    question = data['new_question']
    answer = data['new_answer']
    image = data['image_description']
    prompt = f"Qustion:{question}\nAnswer:{answer}\nImage description:{image}"
    return prompt

def gen_image(data, args):
    start_time = time.time()
    prompt = construct_prompt(data, args)
    res_list = []
    for idx in range(0, args.gen_num):
        new_data = data.copy()
        new_data['id'] = f"{data['id']}_{data['second_idx']}"
        new_data['third_idx'] = idx
        new_id = f"{new_data['id']}_{new_data['third_idx']}"
        if args.dataset in ["geoqa", "geo3k", 'unigeo_proving']:
            gpt4_system_prompt = gpt4_geoqa_system_prompt
        else:
            print("[Warning]Unsupport dataset")
            print("[Warning]Using defalut prompt")
            gpt4_system_prompt = gpt4_geoqa_system_prompt
        response = gpt4_api((gpt4_system_prompt, prompt, args.api_key, args.gen_num, args.max_retry_num))
        code = find_code(response)
        code_path = os.path.join(args.code_dir, f"{new_id}.wls")
        image_path = os.path.join(args.image_dir, f"{new_id}.png" )
        res_list.append((code ,code_path, image_path, response, new_data, args))
    end_time = time.time()
    print("requstion time = ", end_time - start_time)
    return res_list
        
def setcallback(x):
    for data in x:
        code ,code_path, image_path, response, new_data, args = data
        try:
            is_success = run_code(code, code_path, image_path)
            print("is_success = ", is_success)
        except:
            print("[Error]response = ", response)
            print("[Error]code = ", code)
        
        new_data['code_path'] = code_path
        new_data['image_path'] = image_path
        with open(args.output_file, "a") as file:
            file.write(json.dumps(new_data, ensure_ascii=False))
            file.write('\n')
        time.sleep(2)
        
if __name__ == '__main__':
    args = get_args()
    # makedir
    output_dir = os.path.dirname(args.output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    if not os.path.exists(args.code_dir):
        os.makedirs(args.code_dir)
    if not os.path.exists(args.image_dir):
        os.makedirs(args.image_dir)
    #read file
    instruction_list = read_jsonl(args.instruction_file)
    full_id = [f"{data['id']}_{data['second_idx']}" for data in instruction_list]
    # remove finished id
    if os.path.exists(args.output_file):
        finish_list = read_jsonl(args.output_file)
        finish_id = [data['id'] for data in finish_list]
        unfinish_id = [id for id in full_id if id not in finish_id]
    else:
        unfinish_id = full_id
    
    unfinish_instruction_list = [data for data in instruction_list if f"{data['id']}_{data['second_idx']}" in unfinish_id]
    pool = multiprocessing.Pool(args.mp_num)
    for data in tqdm(unfinish_instruction_list):
        pool.apply_async(func=gen_image, args=(data, args), callback=setcallback)
    pool.close()
    pool.join()