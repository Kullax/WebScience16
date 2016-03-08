# -*- coding: utf-8 -*-
import sys
import re
import string

stopwords = []
trends = []

def get_stopwords():
    """
    Creates a list of unique stopwords from the textfile stopwords.txt
    """
    file_dest = 'stopwords.txt'
    f = open(file_dest, 'r')
    if f:
     for line in f:
      w = line.split(' ', 1)[0]
      if w not in stopwords:
       stopwords.append(w)
    f.close()

def strip(str):
    """
    Applies 'basic pre-processing' by removing punctuation, stopwords, and ensuring lowercase
    """
    result = ' '.join(filter(lambda x: x.lower() not in stopwords,  str.split()))
    result = result.lower()
    chars = re.escape(string.punctuation)
    white = re.escape(string.whitespace)
    result = re.sub('['+chars+']+', ' ',result)
    return result

def tokenize(type, v):
    """
    Opens a file, either from 'sundhed.dk' or 'ssi.dk', then running stripping it before
    returning a list of words
    """
    dest = ""
    file = ""
    if v == 0:
        file = "descriptions/"+type+"/sundhed_dk.txt"
    else:
        file = "descriptions/"+type+"/ssi_dk.txt"
    f = open(file, 'r')
    output = strip(f.read()) + " "
    f.close()
    return output

def find_trend(text1, text2):
    """
    Compares two tokenized lists, producing a list of unique words which are present in both
    lists
    """
    first_file = []
    for word in text1.split():
      if word not in first_file:
       first_file.append(word)
    for word in text2.split():
        if word in first_file:
            if word not in trends:
                trends.append(word)
    
def run(type):
    """
    Goes through the nessasary steps to produce the trend query list.
    """
    # remove stopwords and other symbols
    get_stopwords()
    # read in description one
    o1 = tokenize(type, 0)
    # read in description two
    o2 = tokenize(type, 1)
    # compare the descriptions
    find_trend(o1, o2)
    # for debugging sake, and since the assignment asked for it, save the query list
    f = open("trends/"+type+"_trends.log", 'w')
    f.write("\n".join(trends))
    f.close()
    # return the query list
    return trends