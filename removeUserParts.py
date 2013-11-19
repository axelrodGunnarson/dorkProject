import os
import sys
import re
import datetime

def check_arguments():
    if len(sys.argv)!=3:
        return False
    if not os.path.exists(sys.argv[1]):
        return False
    return True

def usage():
    print "Usage: %s <sourceDirectory> <destinationDirectory>" %(sys.argv[0])

def removeSt(listOfStrings, cont):
    return [item for sublist in [s.split(cont) for s in listOfStrings] for item in sublist if item]
    
def checkData(st, fmt):
    '''it check if the string match a date object with the passed format, if it is return true, else return False'''
    try:
        datetime.datetime.strptime(st,fmt)
    except ValueError:
        return False
    else:
        return True

def removeSpaces(listOfStrings):
    '''remove initial and final spaces and tabs etc from the st'''
    return [st.strip() for st in listOfStrings]

def removeUserData(listOfStrings):
    '''for all strings in the list split each one according to cont parameter'''
    cont = "AAAAAAAA"
    tmpl=removeSt(listOfStrings, cont)
    return tmpl
    #return st.replace(cont,"")

def removeMonth(listOfStrings):
    longMonths = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    shortMonths = ["Jan", "Feb","Mar", "Apr", "May", "Jul","Aug", "Sep", "Oct", "Nov", "Dec"]
    tmpl=listOfStrings
    for el in longMonths+shortMonths:
        tmpl = removeSt(tmpl,el)
    return tmpl

def removeDay(listOfStrings):
    days=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']
    tmpl=listOfStrings
    tmpl=[el for el in tmpl if el not in days]
#    for el in days:
#        tmpl = removeSt(tmpl,el)
    return tmpl

def removeDayLong(listOfStrings):
    return [el for el in listOfStrings if not checkData(el, "%a, %d")]

def removeTimeLong(listOfStrings):
    return [el for el in listOfStrings if not checkData(el, "%H:%M:%S %z")]

def removeYear(listOfStrings):
    years=['2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019']
    tmpl=listOfStrings
    for el in years:
        tmpl = removeSt(tmpl,el)
    return tmpl

regex_url=re.compile(r'http://192.168.178.160[^ ]*')
def removeUrl(listOfStrings):
    cont="192.168.178.160"
    tmpl=[]
    for el in listOfStrings:
        tmpl.append(regex_url.sub('',el))
    return tmpl

#    return removeSt(listOfStrings, cont)

def ruleLengthString(st):
    '''refuse sts smaller than a certain threshold'''
    threshold=1
    if len(st) <= threshold:
        return False
    return True

def userContentString(st):
    '''refuse st if equal to a certain content'''
    cont="AAAAAAAA"
    if st == cont:
        return False
    return True

#def dateString(st):
#    '''refuse if the string contains a month (long or short version)'''
#    longMonths = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
#    shortMonths = ["Jan", "Feb", "Mar", "Apr", "May", "Jul","Aug", "Sep", "Oct", "Nov", "Dec"]
#    if any(s in st for s in longMonths):
#        return False
#    if any(s in st for s in shortMonths):
#        return False
#    return True
#
#def siteURLString(st):
#    url="192.168.178.160"
#    if url in st:
#        return False
#    return True

listOfActiveRules = [
    ruleLengthString,
    userContentString,
#    dateString,
#    siteURLString,
    ]

listOfNormalization = [
    removeUserData,
    removeUrl,
    removeSpaces,
    removeDay,
    removeMonth,
    removeYear,
    removeDayLong,
    ]

def fileAccepted(listOfStrings):
    st="Apache/2.2.22 (Ubuntu) Server at 192.168.178.160 Port 80"
    for el in listOfStrings:
        if st in el:
            return False
    return True


if not check_arguments():
    usage()
    sys.exit(1)

destDir=sys.argv[2]
for dirpath,dirname,filenames in os.walk(sys.argv[1]):
        for name in filenames:
            path = os.path.join(dirpath, name)
            tmpPage = [s for s in open(path).readlines()]
            if fileAccepted(tmpPage):
                for f in listOfNormalization:
                    tmpPage = f(tmpPage)
                finalPage = set([s for s in tmpPage if all(rule(s) for rule in listOfActiveRules)])
                dstPath = os.path.join(destDir, name)
                print "analyzed %s: %d line added" %(path, len(finalPage))
                try:
                    f=open(dstPath, "w")
                    for s in finalPage:
                        print >>f, s
                except OSError:
                    print "PANIC: impossible to open file %s" %(dstPath)
