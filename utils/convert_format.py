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

from utils.data_process import read_jsonl, write_jsonl, write_json

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file', type=str)
    parser.add_argument('--output_file', type=str)
    parser.add_argument('--model', type=str)

if __name__ == '__main__':
    args = get_args()
    input_data = read_jsonl(args.input_file)
    output_data = []
    for data in tqdm(input_data):
        new_data = {}
        new_data['id'] = data['id']
        if args.model in ['llava', 'sharegpt4v', 'internvl_chat']:
            new_data['image'] = data['image']
            conversations = []
            for conv in data['conversations']:
                if conv['from'] == 'user':
                    conversations.append({"from":'human', 'value':conv['value'].replace("<ImageHere> ", "<image>\n")})
                else:
                    conversations.append({"from":'gpt', 'value':conv['value'].replace("<ImageHere> ", "<image>\n")})
            new_data['conversations'] = conversations
        else:
            print("[Error]Unsupport model")
            exit()
        output_data.append(new_data)
    if args.output_file.endswith(".jsonl"):
        write_jsonl(args.output_file, output_data)
    elif args.output_file.endswith(".json"):
        write_json(args.output_file, output_data)
    else:
        print('[Error]Unsupport filename')