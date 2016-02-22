#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import re
import string

stopwords = []
trends = []

def get_stopwords():
    file_dest = '../sources/stopwords.txt'
    f = open(file_dest, 'r')
    if f:
     for line in f:
      w = line.split(' ', 1)[0]
      if w not in stopwords:
       stopwords.append(w)
    f.close()

def strip(str):
    result = ' '.join(filter(lambda x: x.lower() not in stopwords,  str.split()))
    result = result.lower()
    chars = re.escape(string.punctuation)
    white = re.escape(string.whitespace)
    result = re.sub('['+chars+']+', ' ',result)
    return result

def tokenize(file):
    f = open(file, 'r')
    output = ""
    for line in f:
     output += strip(line) + " "
    f.close()
    dest = file + "_records.log"
    with open(dest, "w+") as f:
     f.write(output)
    f.close()

def find_trend(file1, file2):
    first_file = []
    f = open(file1, 'r')
    for line in f:
     for word in line.split():
      if word not in first_file:
       first_file.append(word)
    f.close()

    f = open(file2, 'r')
    for line in f:
     for word in line.split():
      if word in first_file:
       if word not in trends:
        trends.append(word)
    f.close()

    with open("trends.txt", "w+") as f:
      f.write(str.join(",", trends))
    f.close()
    
def main():
    get_stopwords()
    if(len(sys.argv) == 3):
        file1 = sys.argv[1]
        file2 = sys.argv[2]
    else:
        file1 = "descriptions/MFR.txt"
        file2 = "descriptions/MFR_sundhed.txt"
    tokenize(file1)
    tokenize(file2)
    find_trend(file1+"_records.log", file2+"_records.log")

if __name__ == "__main__":
    main()