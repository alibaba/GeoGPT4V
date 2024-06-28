from tqdm import tqdm
import requests
import time
from multiprocessing import Pool   
import base64

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
    
def gpt4_api(args):
    system_prompt, user_prompt, api_key, gen_num, max_retry_num = args
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    payload = {
        "model": "gpt-4-turbo-preview",
        "messages": messages,
        "max_tokens": 4096,
        "temperature": 0.8,
    }
    while max_retry_num >= 0:
        request_result = None
        try:
            request_result = requests.post(url, headers=headers, json=payload)
            result_json = request_result.json()
            if 'error' not in result_json: 
                model_output = result_json['choices'][0]['message']['content']
                return model_output.strip()
            else:
                max_retry_num -= 1
        except:
            if request_result is not None:
                print("[warning]request_result = ", request_result.json())
                time.sleep(3)
            else:
                print("[warning]request_result = NULL")
            max_retry_num -= 1

    return ""

def gpt4v_api(args):
    system_prompt, user_prompt, image_path, api_key, gen_num,max_retry_num = args
    base64_image = encode_image(image_path)
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
    }
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": [{
                "type": "text",
                "text": user_prompt
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}",
                    "detail": "high"
                }
            }]
        },
    ]
    payload = {
        "model": "gpt-4-vision-preview",
        "messages": messages,
        "max_tokens": 4096,
        "temperature": 0.8,
    }
    while max_retry_num >= 0:
        request_result = None
        try:
            request_result = requests.post(url, headers=headers, json=payload)
            result_json = request_result.json()
            if 'error' not in result_json: 
                model_output = result_json['choices'][0]['message']['content']
                return model_output.strip()
            else:
                max_retry_num -= 1
        except:
            if request_result is not None:
                print("[warning]request_result = ", request_result.json())
                time.sleep(6)
            else:
                print("[warning]request_result = NULL")
            max_retry_num -= 1
    return ""


