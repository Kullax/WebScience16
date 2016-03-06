# -*- coding: utf-8 -*-
import sys
import re
import string
import tokenizer
import time
from random import randint
import codecs

from pytrends.pyGTrends import pyGTrends

type = "PCV"
trends = []
def run():
    google_username = "wsdnur@gmail.com"
    google_password = "UHac3629"
    path = "trends/"+type+"/"

    # connect to Google
    connector = pyGTrends(google_username, google_password)

    for w in trends:
        print("Running %s" % ""+w)
        # make request
        connector.request_report(str(w), hl='dk', geo='DK', date="today 146-m")

        # wait a random amount of time between requests to avoid bot detection
        time.sleep(randint(5, 10))
        # file names should avoid danish specialcases
        name=w.replace('ø','oe').replace('æ','ae').replace('å','aa')
        # download file
        connector.save_csv(path, name)

if __name__ == "__main__":
    if(len(sys.argv) > 1):
        type = sys.argv[1]
    trends = tokenizer.run(type)
    run()