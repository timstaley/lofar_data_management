#!/usr/bin/python
from folder_property_keys import FKey, hdrs

import os, sys, subprocess
import csv

def main():
    if (len(sys.argv) < 2):
        print "Usage: stat_folder outfile.csv infile1.csv [infile2.csv ...]"
        return 1
    
    outfile_path = sys.argv[1]
    infiles = sys.argv[2:]
    
    data=[]
    
    for path in infiles:
        with open(path) as f:
            rdr = csv.DictReader(f, hdrs.keys())
            for dictrow in rdr:
                data.append(dictrow)
            
    with open(outfile_path, 'w') as f:
        writer = csv.DictWriter(f, hdrs.keys())
        writer.writerow(hdrs)
        for fd in data:
            writer.writerow(fd)
    
if __name__=='__main__':
    sys.exit(main())    