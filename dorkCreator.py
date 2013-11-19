import os
import sys
import json

url="192.168.178.160"
orig_ch = u'_AAA_'
def check_arguments():
    if len(sys.argv)!=3:
        return False
    if not os.path.exists(sys.argv[1]):
        return False
    return True

def usage():
    print "Usage: %s <sourceDirectory> <destinationFile>" %(sys.argv[0])

if not check_arguments():
    usage()
    sys.exit(1)

sourceDir = sys.argv[1]
destFile = sys.argv[2]
dictOfDorks={}
for dirpath,dirname,filenames in os.walk(sys.argv[1]):
    for name in filenames:
        path=os.path.join(dirpath,name)
        f=set([s.strip() for s in open(path).readlines()])
        path = path.split(url)[1].replace(orig_ch, u"/")
        dictOfDorks[path]=list(f)
#     ob = {"listOfPath":[path], "listOfDork":f}
        #item already there
  #      for obj in dictOfDorks:
  #          if f==dictOfDorks[obj]["listOfDork"]:
  #              dictOfDorks[obj]["listOfPath"].append(path)
  #              break
  #      else:
  #          dictOfDorks[path] = ob
f=open(destFile,"w")
#    for path in dictOfDorks[el]["listOfPath"]:
#        print >>f, path+":"
#    st='"'+'" AND "'.join(dictOfDorks[el]["listOfDork"])+'"'
#    print >>f, st
json.dump(dictOfDorks,f)
