# -*- coding: utf-8 -*-
"""
Created on Wed May  9 18:56:19 2018

@author: user
"""

def time_at_point(dataformat, X):
    X_valueSe = np.int(X)
    X_valueMi = X - X_valueSe
    #X_valueSe,X_valueMi=X.split(".")
    #print(X_valueSe,X_valueMi)    
    tp = dataformat + timedelta(seconds = X_valueSe, microseconds=X_valueMi)
    #tp = 0
    return tp