# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 18:48:13 2018

@author: user
"""
import csv
import sys
import numpy as np
import matplotlib.pyplot as plt
#file info
filepath="D:\Idean\Smart meter\location_001_dataset_001\location_001_ivdata_001.txt"
with open(filepath,'rt') as fileobj:
    cin = csv.reader(fileobj)
    datas = [row for row in cin]


count=23+5000*100 #as least 23
#scale: 50k->4.18 100k->8.34 1M->83.4
if count < 23:
    #print('Pleas set the start value more than 22 (at least 23)' )
    sys.exit("Pleas set the start value more than 22 (at least 23)")

rl=1000*40
#scale: 1000->5period

if rl+count >len(datas):
    sys.exit("Out of range -> datas lenth just 1249223")
X_value = np.arange(rl,dtype = np.float)
Phase_A = np.arange(rl,dtype = np.float)
for i in range(rl):
    X_value[i]=datas[i+count][0]
    Phase_A[i]=datas[i+count][1]

plt.figure(figsize=(22,13),num='startmeter') 
plt.plot(X_value,Phase_A)
plt.show()

    #general [papar]