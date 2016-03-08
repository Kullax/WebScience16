# -*- coding: utf-8 -*-
#importing pytrends and dependencies
import time
from random import randint
from pytrends.pyGTrends import pyGTrends

import re
import numpy as np
from matplotlib import pyplot as plt

#importing prediction tool
from sklearn import cross_validation, linear_model
from sklearn.metrics import mean_squared_error

# import other written code modules needed
import tokenizer, regular


# Temp list for creating X for Lasso
def run(type, online=True):
    # Lasso Prediction - tolerance set to avoid converge warning
    model = linear_model.Lasso(tol=0.001)

    tmp = []
    google_username = "xxx@gmail.com" # We Be Anomynous
    google_password = "yyyyyy"
    # Location for .csv
    path = "trends/"+type+"/"

    # Using pytrends for gathering data from Google - but only if online, else uses local data
    # connect to Google
    if online:
        connector = pyGTrends(google_username, google_password)
    # tokenizer will determine the trends needed
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
        months = regular.GetArrayFromFile(""+path+name+".csv")
        if months != None:
            tmp.append(months)
    # Convert the tmp list to a numpy array of proper dimension
    X = np.array(tmp).transpose()
    # Extract clinical data
    json_pattern = re.compile('[0-9]+\.[0-9]+')
    f = open("vactionations/"+type+"-1.json", "r")
    data = f.read()
    f.close()
    match = json_pattern.findall(data)
    # Y is now the clinical data
    Y = np.array([float(x) for x in match][0:len(X)])
    # Preform 5-fold crossvalidation
    k_fold = cross_validation.KFold(len(X), 5)
    v = 0
    plt.figure(type + " 5-fold graphs")
    for k, (train, test) in enumerate(k_fold):
        model.fit(X[train], Y[train])
        plot_y = model.predict(X[test])
        plt.subplot(5, 1, k+1)
        plt.ylabel("Fold %s" % (k+1))
        plot_x = range(len(plot_y))
        plt.plot(plot_x, plot_y, color='b', label='Prediction')
        plt.plot(plot_x, Y[test], color='r', label='Clinical')
        # RMSE for each fold is summed
        RMSE = mean_squared_error(Y[test],plot_y)
        v += RMSE
        print test
    # overall RMSE is determined
    print type, "RMSE", np.sqrt(v/5)
    # For fun, a full prediction is made, to compare the model after 5 folds
    # and the ground truth data
    plt.xlabel("Months")
    plt.show()
    plt.figure(type + " full prediction")
    plot_y = model.predict(X)
    plot_x = range(len(plot_y))
    plt.plot(plot_x, plot_y, color='b', label='Prediction')
    plt.plot(plot_x, Y, color='r', label='Clinical')
    plt.xlabel("Months")
    plt.legend(loc="upper right", fancybox=True)
    plt.show()
    

if __name__ == "__main__":
    type = "PVC"
    run(type, False)
    type = "HPV"
    run(type, False)

