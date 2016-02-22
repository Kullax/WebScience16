#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

stopwords = []
file_dest = '../sources/stopwords.txt'
if(len(sys.argv) > 1):
 f = open(sys.argv[1], 'r')
else:
 f = open(file_dest, 'r')

if f:
 for line in f:
  w = line.split(' ', 1)[0].decode("utf-8")
  if w  not in stopwords:
   stopwords.append(w)
# file = sys.argv[0]

#print len(stopwords)
for w in stopwords:
 print w
