import os
import sys
import json
import collections

def check_arguments():
    if len(sys.argv)!=3:
        return False
    if not os.path.exists(sys.argv[1]):
        print "source Directory does not exist"
        return False
    return True

def usage():
    print "Usage: %s <sourceDirectory> <destinationFile>" %(sys.argv[0])
        
        
if not check_arguments():
    usage()
    sys.exit(1)

pathDic={} #key: page || value: times that page compare among all themes
dorkPerPathDic={} #key: page || value: list of dorks present for that page for all themes
#for each page keep a list of its dork (we intend as dork a list of words found inside a page)
numOfThemes=0
for dirpath,dirname,filenames in os.walk(sys.argv[1]):
    for name in filenames:
        pathFile=os.path.join(dirpath,name)
        dic = json.load(open(pathFile))
        for key in dic:
            try:
                pathDic[key]+=1
            except KeyError:
                pathDic[key]=1
            try:
                dorkPerPathDic[key].append(dic[key])
            except KeyError:
                dorkPerPathDic[key]=[dic[key]]
        numOfThemes+=1
'''
General idea is that we have a dict where we have for each page, multiple lists of words.
we want to see, for each page, which words are "real" values or if they are just there because of a theme.
we include a word in the "good dork" list only if its ratio number_present/number_dorks is over a certain threshold
'''


#minNumOfThemes: min number of times a page appear among all themes (study is over 20 themes, so it can go from 0 to 20)
for minNumOfThemes in xrange(0,numOfThemes+1):
    #threshold: threshold for deciding if a word can be included in the final dork for that page or not
    for threshold in (x*0.1 for x in xrange(0,11)):
        newDic={} # key: page || value: words that appear in 
        #iterate over all pages
        for el in dorkPerPathDic:
            #do computations only if that page is present in more than minNumOfThemes themes
            if pathDic[el]>=minNumOfThemes:
                try:
                    a=newDic[el]
                except KeyError:
                    newDic[el]=[]
                #numDorks: number of dorks present for that page (basically it means number of times that page is present in a team)
                numDorks=pathDic[el]
                #list of words (with repetitions) taken from all dorks of a certain page
                listOfWords=[item for sublist in dorkPerPathDic[el] for item in sublist]
                #create dictionary {word: num_of_occurences}
                dictOfWordsCount = collections.Counter(listOfWords)
                #in newDic words that appear in n/m dorks where m is the total number of dorks for that page (that is also the number of time that page is present for each theme)
                for word in dictOfWordsCount:
                    res = float(dictOfWordsCount[word])/numDorks
                    if res >=threshold:
                        newDic[el].append(word)
        print "Testing with threshold %.1f numOfDorks %d" %(threshold, minNumOfThemes)
        print "Num of Paths: %d" %(len(newDic))
        for el in newDic:
            print "#"*90
            print "page: %s" %(el)
            if newDic[el]:
                st='"'+'" AND "'.join(newDic[el])+'"'
                print st.encode('ascii', 'xmlcharrefreplace')
            else:
                print "NONE"

    #    newDic[el]=reduce(set.intersection, dorkPerPathDic[el][1:], set(dorkPerPathDic[el][0]))
    #    for dork in dorkPerPathDic[el]:
    #        if dork not in newDic[el]:
    #            newDic[el].append(dork)

#check number of pages per theme
#for el in pathDic:
#    if pathDic[el] >=minNumOfThemes:
#    print "Num Of Paths: %d" %(pathDic[el])
#        print "#"*90
#        print "page: %s" %(el)
#        st = '"'+'" AND "'.join(newDic[el])+'"'
#        print st.encode('ascii', 'xmlcharrefreplace')
#        for dork in newDic[el]:
#            st='"'+'" AND "'.join(dork)+'"'
#            print st.encode('ascii', 'xmlcharrefreplace')
#for minNumOfThemes in xrange(0,21):
#    tupL= [dorkPerPathDic[s] for s in dorkPerPathDic if pathDic[s]>=minNumOfThemes]
#    print "Total pages: %d" %(len(tupL))
#    for el in tupL:
#        print "%d   %s" %(el[1], el[0])
