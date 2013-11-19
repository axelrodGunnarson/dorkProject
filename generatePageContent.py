import requests
import json
import urlparse
from bs4 import BeautifulSoup, Comment
import re
import sys
import os

'''This script should request for a page, take everyhting outside meta tag and output this result inside a document with the same name as the page'''

def createFile(url):
    u=url
    replacement=u'_AAA_'
    if u.endswith(u"/"):
        u=u[:-1]
    if http_tag.match(u):
        u = http_tag.sub(u"",u)
    u=u.replace(u"/",replacement)
    return u

def check_arguments():
    if len(sys.argv)!=3:
        return False
    if not os.path.exists(sys.argv[1]):
        return False
    if not os.path.exists(sys.argv[2]):
        return False
    return True

def usage():
    print "Usage: %s <fileWithListOfUrls> <destinationDirectory>" %(sys.argv[0])

avoid_mimes=[
    "application/javascript",
    "application/x-javascript",
    "application/x-shockwave-flash",
]

if not check_arguments():
    usage()
    sys.exit(1)

http_tag = re.compile(r'https?://')
direc=sys.argv[2]
listOfWebPages=[u.strip() for u in open(sys.argv[1]).readlines()]
listOfWebPages = [u for u in listOfWebPages if u]
for url in listOfWebPages:
    r=requests.get(url)
    content_type = "binary"
    try:
        content_type=r.headers['content-type'].split(";")[0]
    except AttributeError:
        #no header content-type
        pass
    print "url: %s, MIME: %s, content-length: %s" %(url, content_type,r.headers['content-length'])
    if content_type not in avoid_mimes:
        soup=BeautifulSoup(r.text)
        try:
            body = soup.body(text=True)
        except TypeError:
            #there is no body, probably empty content
            print "PANIC!! NO BODY!!" 
        else:
            comments = soup.findAll(text=lambda text:isinstance(text, Comment))
            [comment.extract() for comment in comments]
            [s.extract() for s in soup('script')]
            body = soup.body(text=True)
            t = [t.strip() for t in body]
            t = [s for s in t if s]
            if t:
                try:
                    f = open(os.path.join(direc,createFile(url)),"w")
                except IOError:
                    pass
                else:
                    for el in t:
                        print >>f, el.encode("utf-8")




