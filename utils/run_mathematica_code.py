from tqdm import tqdm
import os
from utils.regular_function import find_image_code, find_graphics, find_image_path
from utils.wls import write_wls, read_wls, execute_wls

def fix_image_path(code, image_path):
    image_code = find_image_code(code)
    if image_code is None:
        graphic = find_graphics(code)
        if graphic is not None:
            image_code = f"Export[{image_path}, {graphic}]"
            code += f"\n{image_code}"
    else:
        old_image_path = find_image_path(image_code)
        fixed_image_code = image_code.replace(old_image_path, image_path)
        code = code.replace(image_code, fixed_image_code)
        
    return code

def run_code(code, code_path, image_path):
    write_wls(code, code_path)
    fixed_code = fix_image_path(code, image_path)
    write_wls(fixed_code, code_path)
    execute_wls(code_path)
    if os.path.exists(image_path): 
        return True
    else:                          
        return False
    