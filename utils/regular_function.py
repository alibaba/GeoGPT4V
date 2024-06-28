import re

def find_image_code(code):
    pattern = r'Export\[(.*?)\]'
    matches = re.findall(pattern, code)
    if matches:
        return f"Export[{matches[-1]}]"
    else:
        return None

def find_image_path(code):
    pattern = r"(['\"])(.*?)\1"
    matches = re.findall(pattern, code)
    if matches:
        return matches[0][1]
    else:
        return None
    
def find_code(response):
    pattern = r'```(.*?)```'
    matches = re.findall(pattern, response, re.DOTALL)
    if matches:
        code = matches[0]
        code = code.strip()
        if code.startswith("Mathematica") or code.startswith("mathematica"):
            code = code[11:]
            code = code.strip()
        return code
    else:
        if code.startswith("Code:\n"):
            code = code[5:]
            code = code.strip()
            return code
        else:
            return None


def split_qa(response):
    response += '\n'
    pattern = r'New_Question: (.*?)\nNew_Answer: (.*?)\nImage_Description: (.*?)\n'
    matches = re.findall(pattern, response, re.DOTALL)
    qa_pairs = []
    for match in matches:
        question = match[0].strip()
        answer = match[1].strip()
        image_description = match[2].strip()
        qa_pairs.append({
                'question': question, 
                'answer': answer,
                'image_description': image_description
                })
        
    return qa_pairs

def find_score(response):
    response += '\n'
    pattern = r'Score: (.*?)\n'
    matches = re.findall(pattern, response, re.DOTALL)
    if matches:
        return matches[0]
    else:
        return 0
