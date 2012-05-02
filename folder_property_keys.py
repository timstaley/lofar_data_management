import sys

pyversion= float(sys.version[:3])
if pyversion >= 2.7:
    from collections import OrderedDict
else:
    from ordereddict import OrderedDict #requires package installation

def generate_autocomplete_dictionary_keys(dummy_key_class):
    for att_name, att_val in vars(dummy_key_class).iteritems():
        if(att_name[:2]!="__" and att_val==None):
            setattr(dummy_key_class, att_name, "".join([dummy_key_class.__name__,"_",att_name]))

class FKey():
    """Namespace enclosed dictionary keys, used for storing folder information.
        NB. These have the pleasant property that pydev autocompletion will fill them in for you.
    """
    area=None
    name=None
    size=None
    dates=None
    ra=None
    dec=None
    descript=None
    owner=None
    users=None
    active=None
    archived=None
    
generate_autocomplete_dictionary_keys(FKey)

#Column headers for output to a csv.
hdrs=OrderedDict()
hdrs[FKey.area] = "RAID array (A/B/C...)"
hdrs[FKey.name] = "Folder name"
hdrs[FKey.size] = "Size (GB)"
hdrs[FKey.dates] = "Observation dates"
hdrs[FKey.ra] = "RA"
hdrs[FKey.dec] = "Dec"
hdrs[FKey.descript] = "Description"
hdrs[FKey.owner] = "Owner"
hdrs[FKey.users] = "Additional users"
hdrs[FKey.active] = "Actively in use? (Y/N/Unsure)"
hdrs[FKey.archived] = "Archived elsewhere? (Y/N/Unsure)"