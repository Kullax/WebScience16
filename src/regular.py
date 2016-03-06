# -*- coding: utf-8 -*-
import sys
import re
import string
import tokenizer
import numpy as np
    
type = "PCV"
# Pattern for a week .csv
week_pattern = re.compile('\d\d\d\d-\d\d-\d\d\s-\s\d\d\d\d-\d\d-\d\d,[0-9]*')
# Pattern for a month .csv
month_pattern = re.compile('\d\d\d\d-\d\d,[0-9]*')

def WeeksToMonths(data):
    """ 
    Returns a list of montly values, computed from weeks.
    Input: a list of raw weeks, as given by the google csv. file.
    Output: a numpy array with values computed on a montly basis.
    """
    a = ""
    month = 0
    value = 0
    it = 1
    for week in data:
        w, v = week.split(",")
        w = w.split("-")
        if w[1] == month:
            value += float(v)
            it += 1
        else:
            a = a + str(value/it) + ","
            month = w[1]
            # We dont want the empty string.
            if v == "":
                break
            value = float(v)
            it = 1
    a = a + str(value/it)
    a = np.array(a.split(','))
    return a
    
def HandleMonths(data):
    """
    Extracts the values from the raw month data
    Input: List of raw month data as given by the google csv. file
    Output: a numpy array with values for each month
    """
    a = ""
    for month in data:
        m, v = month.split(',')
        a = a + str(v) + ','
    a = np.array(a.split(','))
    return a
    
def GetArrayFromFile(file):
    """
    Takes a .cvs location, and determines if it has monthly or weekly data.
    Then extracts the value, and returns a numpy array.
    """
    f = open(file, "r")#"trends/" + type + "/" + name + ".csv", "r")
    data = f.read()
    f.close()
    m = month_pattern.findall(data)
    if m:
        return HandleMonths(m)
    m = week_pattern.findall(data)
    if m:
        return WeeksToMonths(m)

if __name__ == "__main__":
    if(len(sys.argv) > 1):
        type = sys.argv[1]
    print GetArrayFromFile("trends/" + type + "/alvorlige.csv")
