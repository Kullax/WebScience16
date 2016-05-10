# -*- coding: utf-8 -*-
import xml
import string
import pickle
from sklearn import cross_validation, linear_model
from sklearn.metrics import mean_squared_error
# Module for fixing unicode errors made on the forum, there's a few of these in our data. pip install ftfy
#import ftfy
import json
# pip install gspread
import gspread
# pip install oauth2client==1.5.2 if cannot import name error. Rollbacks are troublesome.
from oauth2client.client import SignedJwtAssertionCredentials
from uclassify import uclassify
import numpy as np
from itertools import chain
from enum import Enum
from operator import itemgetter

class Sentiment(Enum):
    negative = 0
    neutral = 1
    positive = 2

def DownloadReviewData():
    """
    Connects to google drive, and gives access to the spreadsheets
    """
    # Unique json file for Project with Private Copy of Shared Spreedsheet.
    json_key = json.load(open('WebScience2016-825a037eea0f.json'))
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope)
    gc = gspread.authorize(credentials)
    print "Connecting to google drive"
    # Copy of the original spreedsheet.
    wks = gc.open("Sentiment Annotations - WS").sheet1
    print "Retrieving Sentiments"
    sentinent = wks.col_values(2)
    print "Retrieving Reviews"
    reviews = wks.col_values(4)
    r_s = []
    r_r = []
    for sen, rev in zip(sentinent, reviews):
        if rev != "":
            try:
                s = int(sen)
                r_s.append(sen)
                r_r.append(rev)
            except ValueError:
                print "Invalid Sentiment", sen
    with open("rawSentiment", 'wb') as f:
        pickle.dump(r_s, f)
    with open("rawReviews", 'wb') as f:
        pickle.dump(r_r, f)

def DoClassify():
    """
    Remember to start a local server first, as this is an entirely offline approach
    Trains and Evaluates using uClassify
    """
    with open("rawSentiment", 'rb') as f:
        sentiment = pickle.load(f)
        del sentiment[0]
    with open("rawReviews", 'rb') as f:
        review = pickle.load(f)
        del review[0]
    review = np.array([x.encode('ascii', 'ignore') for x in review])
    sentiment = np.array(sentiment)
    classifier_name = "Lego_Review"
    a = uclassify()
    max = 50
    it = 0
    positive = []
    negative = []
    neutral = []
    a.removeClassifier("fold")
#    a.removeClassifier("fold%d"%0)
#    a.removeClassifier("fold%d"%1)
#    a.removeClassifier("fold%d"%2)
#    k_fold = cross_validation.KFold(len(review), 3)
#    for k, (train, test) in enumerate(k_fold):
#        t=0
#        f=0
#        print k
    a.create("fold")
    a.addClass(["Negative", "Neutral", "Positive"],"fold")
    for r,s in zip(review, sentiment):
        try:
            if s == "1":
                positive.append(r)
            elif s == "-1":
                negative.append(r)
            elif s == "0":
                neutral.append(r)
            if len(positive) > 50:
                a.train(positive, "Positive", "fold")
                positive = []
            if len(negative) > 50:
                a.train(negative, "Negative", "fold")
                negative = []
            if len(neutral) > 50:
                a.train(neutral, "Neutral", "fold")
                neutral = []
        except UnicodeEncodeError, ex:
            print "Cannot train; ", ex
    # Any leftover should not be excluded
    if len(positive) > 0:
        a.train(positive, "Positive", "fold")
        positive = []
    if len(negative) > 0:
        a.train(negative, "Negative", "fold")
        negative = []
    if len(neutral) > 0:
        a.train(neutral, "Neutral", "fold")
        neutral = []
    it = 0
    print "testing"
    with open("lego.txt", 'r') as f:
        reviews = f.readlines()
   # while it+50 < 500:
    d = a.classify(reviews,"fold")
    with open("classs.txt", 'w') as f:
        for dd in d:
            f.write(  str(Sentiment(np.array([float(x[1]) for x in dd[2]]).argmax()).value-1) + "\n")
    
#            for dd, ss in zip(d, sentiment[test[it:it+50]]):
                # will take the calculated sentiment, and compare to the ground truth
#                if Sentiment(np.array([float(x[1]) for x in dd[2]]).argmax()).value-1 == int(ss):
                    # if equal, increment true
 #                   t+=1
  #              else:
                    # else increment false
   #                 f+=1
#            it += 50
#        d = a.classify(review[test[it:len(test)]],"fold%d"%k)
 #       print t, f
  #  a.removeClassifier(classifier_name)

def GenerateStanfordData():
    """
    Splits the reviews to manageable pieces for the Stanford NLP.
    And converts the -1,0,1 rating to 01,2,3,4 rating.
    """
    with open("rawSentiment", 'rb') as f:
        sentiment = pickle.load(f)
        del sentiment[0]
    with open("rawReviews", 'rb') as f:
        review = pickle.load(f)
        del review[0]
    review = np.array([x.encode('ascii', 'ignore') for x in review])
    reviews = []
    sentiment = np.array(sentiment)
    k = 98
    with open("ReadyForStanford.txt", 'w') as f:
            for r,s in zip(review, sentiment):
                a = ""
                if s == "-1":
                    a = "0"
                elif s == "0":
                    a = "2"
                elif s == "1":
                    a = "4"
                else:
                    print s
                if len(r) > 200:
                    output = ""
                    for line in r.split("."):
                        if len(output) + len(line) < 200:
                            output = output + " " + line
                        else:
                            if output.strip().translate(string.maketrans("",""), string.punctuation) != "":
                                f.write(a+"\t"+output+"\n\n")
                                reviews.append(output)
                            output = line
                    if output.strip().translate(string.maketrans("",""), string.punctuation) != "":
                        f.write(a+"\t"+output+"\n\n")
                        reviews.append(output)
                else:
                    if r.strip().translate(string.maketrans("",""), string.punctuation) != "":
                        f.write(a+"\t"+r+"\n\n")
                        reviews.append(r)
    # Multilined version of original reviews. Having too big reviews could cause problems.
    with open("rawrReviews", 'wb') as f:
        pickle.dump(reviews, f)

def FoldStanfordData():
    """
    Splits the data tree generated after GenerateStanfordData() was processed by the Stanford Toolkit
    into training and testing sections for 3-fold cross validation.
    """
    # Multilined version of original reviews. Having too big reviews could cause problems.
    with open("rawrReviews", 'rb') as f:
        review = pickle.load(f)
    # tree_non being the name of the GenerateStanfordData function, change to tree_non for non sentiment tree.
    with open("tree_non.txt", 'r') as reviews:
        lines = reviews.readlines()
        k_fold = cross_validation.KFold(len(lines), 3)
        for k, (train, test) in enumerate(k_fold):
            print train, test
            with open("train%d.txt"%k, 'w') as f:
                for t in train:
                    f.write(lines[t]+"\n")
            with open("test%d.txt"%k, 'w') as f:
                for t in test:
                    f.write(lines[t]+"\n")

                    
#with open("rawSentiment", 'rb') as f:
#    sentiment = pickle.load(f)
#print len(sentiment)
# Have internet on for this
#DownloadReviewData()
# Turn on a uClassify Server, and have modified socket access to localhost instead of website
#try:
#    DoClassify()
#except:
#    print "Is server on?"
# Deep-Learning Start here - still depends on DownloadReviewData()
# Makes review and sentiment into a mangeable format for Stanford NLP
#GenerateStanfordData()
# Only run AFTER having produced the Tree Data using the NLP.
#FoldStanfordData()
# Now to training and testing using train.sh script.

#it = 0
#itt = 0
#it0 = 0
#with open("rawSentiment", 'rb') as f:
#    sentiment = pickle.load(f)
#for sen in sentiment:
#    if sen == "1":
#        it += 1
#    if sen == "-1":
#        itt += 1
#    if sen == "0":
#        it0 += 1
#print it, itt, it0
#    del sentiment[0]
DoClassify()
#GenerateStanfordData()