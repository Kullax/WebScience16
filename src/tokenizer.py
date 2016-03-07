# -*- coding: utf-8 -*-
import sys
import re
import string
import codecs

stopwords = []
trends = []

def get_stopwords():
    file_dest = '../sources/stopwords.txt'
    f = open(file_dest, 'r')
    if f:
     for line in f:
      w = line.split(' ', 1)[0]
      if w not in stopwords:
       stopwords.append(str(w))
    f.close()

def strip(str):
    result = ' '.join(filter(lambda x: x.lower() not in stopwords,  str.split()))
    result = result.lower()
    chars = re.escape(string.punctuation)
    white = re.escape(string.whitespace)
    result = re.sub('['+chars+']+', ' ',result)
    return result

def tokenize(type, v):
    dest = ""
    file = ""
    if v == 0:
        file = "descriptions/"+type+"/sundhed_dk.txt"
        dest = "trends/"+type+"_sundhed_dk_records.log"
    else:
        file = "descriptions/"+type+"/ssi_dk.txt"
        dest = "trends/"+type+"_ssi_dk_records.log"
    f = open(file, 'r')
    output = ""
    output += strip(f.read()) + " "
    f.close()
    return output

def find_trend(text1, text2):
    first_file = []
    for word in text1.split():
      if word not in first_file:
       first_file.append(word)
    for word in text2.split():
        if word in first_file:
            if word not in trends:
                trends.append(word)
    
def run(type):
    get_stopwords()
    o1 = tokenize(type, 0)
    o2 = tokenize(type, 1)
    find_trend(o1, o2)
    return trends