#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import re
import string

stopwords = []
file_dest = '../sources/stopwords.txt'
f = open(file_dest, 'r')
if f:
 for line in f:
  w = line.split(' ', 1)[0]
  if w  not in stopwords:
   stopwords.append(w)
f.close()

def strip_everything(str):
 result = ' '.join(filter(lambda x: x.lower() not in stopwords,  str.split()))
 result = result.lower()
 chars = re.escape(string.punctuation)
 white = re.escape(string.whitespace)
 result = re.sub('['+chars+']+', ' ',result)
# result = re.sub('['+whitespace+']+', '',result)
 return result

if(len(sys.argv) > 1):
 f = open(sys.argv[1], 'r')
 output = ""
 for line in f:
  output += strip_everything(line) + " "
 f.close()
 dest = sys.argv[1].replace('.txt', '') + "_records.log"
 with open(dest, "w+") as f:
  f.write(output)
 f.close()
if(len(sys.argv) > 2):
 f = open(sys.argv[2], 'r')
 output = ""
 for line in f:
  output += strip_everything(line) + " "
 f.close()
 dest = sys.argv[2].replace('.txt', '') + "_records.log"
 with open(dest, "w+") as f:
  f.write(output)
 f.close()

first_file = []
trends = []
f = open(sys.argv[1].replace('.txt', '') + "_records.log", 'r')
for line in f:
 for word in line.split():
  if word not in first_file:
   first_file.append(word)
f.close()

f = open(sys.argv[2].replace('.txt', '') + "_records.log", 'r')
for line in f:
 for word in line.split(' '):
  if word in first_file:
   if word not in trends:
    trends.append(word)
f.close()

with open("trends.txt", "w+") as f:
  f.write(str.join(",", trends))
f.close()
