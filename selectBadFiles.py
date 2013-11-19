import os
import sys
import magic
import re

deleteFiles= [
    "empty",
    "data",
    "Web Open Font Format",
]
badFileNames = [
    r"license",        
    r"copying",
    r"readme",
    r'changelog.txt',
    r'wp-mce-help.php',
    r'.css'
]

def check_arguments():
    if len(sys.argv)!=3:
        return False
    if not os.path.exists(sys.argv[1]):
        return False
    if not os.path.exists(sys.argv[2]):
        return False
    return True

def usage():
    print "Usage: %s <sourceDirectory> <destinationDirectory>" %(sys.argv[0])

if not check_arguments():
    usage()
    sys.exit(1)
filenames_regex = [re.compile(r,flags=re.IGNORECASE) for r in badFileNames]

basePathDst = sys.argv[2]
for dirpath,dirname,filenames in os.walk(sys.argv[1]):
    for name in filenames:
        path=os.path.join(dirpath,name)
        new_path=os.path.join(basePathDst, name)
        typ=magic.from_file(path)
        if any(x in typ for x in deleteFiles):
            os.rename(path,new_path)
        elif any(s.search(name) for s in filenames_regex):
            os.rename(path,new_path)
