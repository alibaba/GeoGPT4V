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

from utils.data_process import read_jsonl
from utils.gpt_api import gpt4_api, gpt4v_api
from utils.regular_function import split_qa
from constant.gen_instruction_prompt import gpt4v_geoqa_system_prompt
import multiprocessing


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--question_file', type=str)
    parser.add_argument('--output_file', type=str)
    parser.add_argument('--api_key', type=str)
    parser.add_argument('--model', type=str, default='gpt4v')
    parser.add_argument('--dataset', type=str, default='geoqa')
    parser.add_argument('--gen_num', type=int, default=1)
    parser.add_argument('--max_retry_num', type=int, default=5)
    parser.add_argument('--mp_num', type=int, default=1)
    return parser.parse_args()

def construct_choice(choice_list):
    num2label = ['A', "B", "C", "D"]
    choice_str = ""
    for idx, choice in enumerate(choice_list):
        choice_str += f"\n{num2label[idx]}. {choice}"
    return choice_str

def construct_prompt(data, args):
    if args.dataset in ["geoqa", 'geo3k']:
        question = data['question']
        choice_str = construct_choice(data['choices'])
        answer = data['answer']
        prompt = f"Qustion:{question} Choices:{choice_str}\nAnswer:{answer}"
    elif args.dataset in ['unigeo_proving']:
        question = data['question']
        answer = data['answer']
        prompt = f"Qustion:{question}\nAnswer:{answer}"
    else:
        print("[Error]Unsupport dataset")
        exit()
    return prompt
            
def gen_instruction_gpt4v(data, args):
    start_time = time.time()
    user_prompt = construct_prompt(data, args)
    if 'image' not in data:
        data['image'] = data['image_path']
    image_path = data['image']
    qa_pairs = []
    if args.dataset in ["geoqa", "geo3k", 'unigeo_proving']:
        gpt4v_system_prompt = gpt4v_geoqa_system_prompt
    else:
        print("[Warning]Unsupport dataset")
        print("[Warning]Using defalut prompt")
        gpt4v_system_prompt = gpt4v_geoqa_system_prompt
    response = gpt4v_api((gpt4v_system_prompt, user_prompt, image_path, args.api_key, args.gen_num, args.max_retry_num))
    qa_pairs = split_qa(response)
    end_time = time.time()
    print("requstion time = ", end_time - start_time)
    return (qa_pairs, data, args)

def setcallback(x):
    qa_pairs, data, args = x
    with open(args.output_file, 'a') as file:
        for idx, qa in enumerate(qa_pairs):
            new_data = data.copy()
            new_data['new_question'] = qa['question']
            new_data['new_answer'] = qa['answer']
            new_data['image_description'] = qa['image_description']
            new_data['second_idx'] = idx
            file.write(json.dumps(new_data, ensure_ascii=False))
            file.write('\n')
    
if __name__ == '__main__':
    args = get_args()
    # makedir
    output_dir = os.path.dirname(args.output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    question_list = read_jsonl(args.question_file)
    
    full_id = [data['id'] for data in question_list]
    # remove finished id
    if os.path.exists(args.output_file):
        finish_list = read_jsonl(args.output_file)
        finish_id = [data['id'] for data in finish_list]
        unfinish_id = [id for id in full_id if id not in finish_id]
    else:
        unfinish_id = full_id
    
    unfinish_list = [data for data in question_list if data['id'] in unfinish_id]
    pool = multiprocessing.Pool(args.mp_num)
    if args.model == 'gpt4v':
        for data in tqdm(unfinish_list):
            pool.apply_async(func=gen_instruction_gpt4v, args=(data, args), callback=setcallback)
        pool.close()
        pool.join()
    else:
        print("[Error]Unsupport model")