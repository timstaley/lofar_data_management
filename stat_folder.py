#!/usr/bin/python
from folder_property_keys import FKey, hdrs

import os, sys, subprocess
import csv

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
    return uid_user_dict[os.stat(path).st_uid]


def main():
    if (len(sys.argv) != 3):
        print "Usage: stat_folder /path/to/folder outfile.csv"
        return 1
    
    parent_folder=sys.argv[1]
    outfile_path = sys.argv[2]
    
    uid_user_dict = get_uid_user_dict()
    
    disk_area = os.path.basename(parent_folder)
    
    subfolders = [ name for name in os.listdir(parent_folder) if os.path.isdir(os.path.join(parent_folder, name)) ]
    
    folder_dicts=[]
    
    for sf in subfolders:
        path = parent_folder+sf
        d = {}
        d[FKey.area] = parent_folder
        d[FKey.name] = sf
        kb = get_folder_size_kb(path)
        d[FKey.size] = kb /(1024.0**2) #Gigabytes
        d[FKey.owner] = get_path_owner(path, uid_user_dict)
        folder_dicts.append(d)
        
    with open(outfile_path, 'w') as f:
        writer = csv.DictWriter(f, hdrs.keys())
        for fd in folder_dicts:
            writer.writerow(fd)
        
if __name__=='__main__':
    sys.exit(main())    



