#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import re
import string
import tokenizer
import time
from random import randint

from pytrends.pyGTrends import pyGTrends

tokenizer.main()

with open("trends.txt", "r") as f:
    line = f.read()
    f.close()
trends = line.split(',')

#i = 0
#while i < len(trends):
#nprint " ".join(trends[0:5])

for word in trends:
    #print trends
    google_username = "wsdnur@gmail.com"
    google_password = "UHac3629"
    path = "trends/"

    # connect to Google
    connector = pyGTrends(google_username, google_password)

    # make request
    connector.request_report(""+word, hl='dk', geo='DK')

    # wait a random amount of time between requests to avoid bot detection
    time.sleep(randint(5, 10))

    # download file
    connector.save_csv(path, ""+word.decode('utf-8'))

    # get suggestions for keywords
    #keyword = "milk substitute"
    #data = connector.get_suggestions(keyword)
    #print(data)