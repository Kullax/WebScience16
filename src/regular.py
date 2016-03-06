# -*- coding: utf-8 -*-
import sys
import re
import string
import tokenizer

type = "PCV"

def run():   
    f = open("trends/" + type + "_trends.txt", "r")
    line = f.read()
    f.close()
    trends = line.split(',')

    for w in trends:
        print w,
        name=w.replace('ø','oe').replace('æ','ae').replace('å','aa')
        f = open("trends/" + type + "/" + name + ".csv", "r")
        data = f.read()
        p = re.compile('(\d{4}-\d{2},[0-9]*)')
        m = p.findall(data)
#%        p = re.compile('/(\d{4}-\d{2},[0-9]*)\n/g')
#"        m = p.search(data)
        if m:
            print "yea", m[0][0:10]
        else:
            print "No"
        f.close()

if __name__ == "__main__":
    if(len(sys.argv) > 1):
        type = sys.argv[1]
    run()
