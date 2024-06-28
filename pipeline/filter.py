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

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file', type=str)
    parser.add_argument('--output_file', type=str)
    parser.add_argument('--threshold', type=str)
    return parser.parse_args()

if __name__ == '__main__':
    args = get_args()
    input_data = read_jsonl(args.input_file)
    print("input data size = ", len(input_data))
    output_data = [data for data in input_data if data['score'] >= args.threshold]
    print("output data size = ", len(input_data))
    write_jsonl(args.output_file, output_data)
    
    
