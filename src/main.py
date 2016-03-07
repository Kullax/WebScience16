# -*- coding: utf-8 -*-
import sys, re
import string
import time
from random import randint
import codecs
import numpy as np
from matplotlib import pyplot as plt
from sklearn import cross_validation, linear_model
import tokenizer, regular
from pytrends.pyGTrends import pyGTrends
from sklearn.metrics import mean_squared_error

# Lasso Prediction
model = linear_model.Lasso()
# Temp list for creating X for Lasso
a = []
def run(type, online=True):
    google_username = "xxx@gmail.com" # We Be Anomynous
    google_password = "yyyyyy"
    path = "trends/"+type+"/"

    # connect to Google
    if online:
        connector = pyGTrends(google_username, google_password)
    for trend in tokenizer.run(type):
        # file names should avoid danish specialcases
        name=trend.replace('ø','oe').replace('æ','ae').replace('å','aa')
        if online:
            # make request
            connector.request_report(str(trend), hl='dk', geo='DK', date="01/2011 57m")
            # wait a random amount of time between requests to avoid bot detection
            time.sleep(randint(3, 6))
            # download file
            connector.save_csv(path, name)
        # Once a csv file has been recovered. Extract the monthly information
        d = regular.GetArrayFromFile(""+path+name+".csv")
        if d != None:
            a.append(d)
    X = np.array(a).transpose()
    json_pattern = re.compile('[0-9]+\.[0-9]+')
    f = open("vactionations/"+type+"-1.json", "r")
    data = f.read()
    f.close()
    m = json_pattern.findall(data)
    Y = np.array([float(x) for x in m][0:len(X)])
    model.fit(X, Y)
    print model.predict(X)
    folds = []
    k_fold = cross_validation.KFold(len(X), 5)
    s = np.array([sum(x)/len(X[0]) for x in X])
    v = 0
    for k, (train, test) in enumerate(k_fold):
        model.fit(X[train], Y[train])
        folds = model.score(X[test], Y[test])
        plot_y = model.predict(X[test])
        plt.subplot(5, 1, k+1)
        plt.ylabel("Fold %s" % (k+1))
        plot_x = range(len(plot_y))
        plt.plot(plot_x, plot_y, color='b')
        plt.plot(plot_x, Y[test], color='r')
        RMSE = mean_squared_error(Y[test],plot_y)
        v += RMSE
    print np.sqrt(v/5)
    plt.xlabel("Months")
    plt.show()
    

if __name__ == "__main__":
    type = "PVC"
    run(type, False)
    type = "HPV"
    run(type, False)

