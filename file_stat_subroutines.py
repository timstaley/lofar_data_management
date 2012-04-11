import os
import subprocess

def get_uid_user_dict():
    d={}
    with open("/etc/passwd") as f:
        lines = f.readlines()
        for l in lines:
            tokens = l.split(':')
            d[int(tokens[2])] = tokens[0]
    return d
            

def get_folder_size_kb(folderpath):
    outstr=[]
    child = subprocess.Popen(["du", "-s", folderpath], stdout=subprocess.PIPE)
    result = child.communicate()
    return int(result[0].split()[0])

def get_path_owner(path, uid_user_dict):
    try:
        return uid_user_dict[os.stat(path).st_uid]
    except OSError:
        return "NotFound"
        
    

def ensure_dir(filename):
    d = os.path.dirname(filename)
    if len(d) and not os.path.exists(d):
        os.makedirs(d)