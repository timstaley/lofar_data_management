#!/usr/bin/python
import os,sys
import re
import csv
import copy

from file_stat_subroutines import *

class Dupe():
    def __init__(self):
        self.byte_size=None
        self.n_copies=None
        self.filename=None
        self.lofar_obs_id=None
        self.lofar_subband=None
        self.locations=[]
        self.owners=[]
    
    def megabytes(self):
        return self.byte_size/(1024.0**2)
    def gigabytes(self):
        return self.byte_size/(1024.0**3)
    
    def wastage(self):
        return self.gigabytes()* (self.n_copies-1)
    
    def __str__(self):
        return str(( "%15.2f" % (self.megabytes(),), 
                     self.n_copies, 
                     str(self.lofar_obs_id),
                     str(self.lofar_subband),
                     ))

def get_self_dupes(user, dupes_list):
    self_dupes=[]
    for d in dupes_list:
        user_count=0
        assert isinstance(d, Dupe)
        for u in d.owners:
            if u == user:
                user_count += 1
        if user_count >= 2:
            sdupe = copy.deepcopy(d)
            sdupe.n_copies = user_count
            sdupe.owners=[]
            sdupe.locations=[]
            for u, l in zip(d.owners, d.locations):
                if u ==user:
                    sdupe.owners.append(u)
                    sdupe.locations.append(l)
            self_dupes.append(sdupe)
    return self_dupes

def write_dupes_csv(dupe_list, outfile_path):
    ensure_dir(outfile_path)
    outfile = open(outfile_path,'wb')
    writer = csv.writer(outfile)
    
    writer.writerow(["wastage (gb)", "filesize(gb)", "copies", 
                     "Obs_id", "sub_band", 
                     "filename", "locations"])
    
    for d in dupe_list:
        user_locs = [str(u)+': '+str(l) for u,l in zip(d.owners, d.locations)]

        writer.writerow([d.wastage(), d.gigabytes(), d.n_copies,
                         d.lofar_obs_id, d.lofar_subband,
                         d.filename
                         ]+
                        user_locs
#                        d.owners+
#                        d.locations
                        )

def main():
    if (len(sys.argv) != 2):
        print "Usage: parse_fslint /path/to/findup_output.txt"
        return 1

    findup_output_path = sys.argv[1]    
    
    uid_user_dict = get_uid_user_dict()
    dupes_file = open(findup_output_path,'r')
    
    dupes = []
    
    for line in dupes_file:
        tokens=line.split()
        d=Dupe()
        d.n_copies = int(tokens[0])
        d.byte_size = int(tokens[2])
        d.locations = tokens[3:]
        d.filename = os.path.basename(d.locations[0])
        oid = re.search('L([0-9]+?)_', d.locations[0])
        if oid:
            d.lofar_obs_id = oid.group(1)
        sb = re.search('_SB(.+?)_', d.locations[0])
        if sb:
            d.lofar_subband = sb.group(1)
        for loc in d.locations:
            d.owners.append(get_path_owner(loc, uid_user_dict))
        
        dupes.append(d)
        
    users = set()
    for d in dupes:
        for u in d.owners:
            users.add(u)
    
    write_dupes_csv(dupes, 'all_dupes.csv')
    total_wastage=0
    for d in dupes:
        total_wastage +=d.wastage()
    print "Total wastage:", ( "%15.2f" % total_wastage)

    self_wastage=0
    for u in users:
        user_self_dupes = get_self_dupes(u, dupes)
        write_dupes_csv(user_self_dupes, "user_self_dupes/"+u+".csv")
        user_self_wastage=0
        for d in user_self_dupes:
            user_self_wastage +=d.wastage()
        print ("Selfwastage for "+u+":").ljust(40),( "%15.2f" %  user_self_wastage )
        self_wastage += user_self_wastage

    print "Total selfwastage", ( "%15.2f" % self_wastage)
    


if __name__=='__main__':
    sys.exit(main())    
