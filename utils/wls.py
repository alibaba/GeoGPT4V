import subprocess

def read_wls(code_path):
    with open(code_path, "r") as file:
        wls = file.read()
    return wls

def write_wls(code, code_path):
    if not code.startswith("#!/usr/bin/env wolframscript"):
        wls = f"#!/usr/bin/env wolframscript\n(* ::Package:: *)\n{code}"
    else:
        wls = code
    with open(code_path, "w") as file:
        file.write(wls)
    
def execute_wls(code_path):
    chmod_command = f"chmod 777 {code_path}"
    result = subprocess.run(chmod_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    run_command = f"{code_path}"
    result = subprocess.run(run_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result