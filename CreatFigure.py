# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 18:48:13 2018

@author: user
"""
"""" define the filter paraeter"""
#fs = 1200
class butter:
    pass
def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y





""" define data time return """
def time_at_point(dataformat, X):
    X_valueSe,X_valueMi=X.split(".")    
    tp = dataformat + timedelta(seconds = int(X_valueSe), microseconds=int(X_valueMi))
    return tp


""" Survey event """
def survey_event(start, y, length, nl):
    for i in range(start,length,1):
        if y[i] > 1:
            time = time_at_point(dataformat,X_value[i])
            if start > nl:
                noise = np.mean(np.absolute(y[i-nl:i:1]))
            else:
                noise = np.mean(np.absolute(y[0:start:1]))
            print(noise,start)    
            for j in range(i+600,length-600, 1):
                end = np.mean(np.absolute(np.array(y[j:j+600:1])))
                #print(end,j,i)
                if end < noise*1.5: 
                    delta = j-i
                    print(delta)
                    return i, time, delta
                elif noise > 1:
                    return i, time, delta
              
        else:
            return 0, 0, 0
"""Example to get specify data time   
 
delaytime=0
delta = dataformat + timedelta(seconds = X_valueSe[delaytime], microseconds=X_valueMi[delaytime])
print(X_valueSe[delaytime],X_valueMi[delaytime])
print(datas[16][1],delta)
"""

import csv
from datetime import datetime
from datetime import timedelta
import numpy as np
from scipy import fftpack
from scipy.signal import butter, lfilter, freqz
import matplotlib.pyplot as plt
filenum=220#248
filepath="D:\Idean\Smart meter\location_001_dataset_001\location_001_ivdata_"+str(filenum)+".txt"
with open(filepath,'rt') as fileobj:
    cin = csv.reader(fileobj)
    datas = [row for row in cin]

#11:58:32.6234999999996440291
dataTime,microsecond=datas[10][1].split(".")
microsecond = microsecond[0:6]  
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
dataformat = datetime.strptime('2011-11-20 '+dataTime+'.'+microsecond,DATETIME_FORMAT)

#print(dataformat,time_at_point)
#Modify area: 
count=23
rl=len(datas)-count#

if count < 23:
    #print('Pleas set the start value more than 22 (at least 23)' )
    sys.exit("Pleas set the start value more than 22 (at least 23)")


if rl+count >len(datas):
    sys.exit("Out of range -> datas lenth just 1249223")


""" Read file in """
X_value = []
Phase_A = np.arange(rl,dtype = np.float)
Phase_B = np.arange(rl,dtype = np.float)
Voltage = np.arange(rl,dtype = np.float)
for i in range(rl):
    X_value.append(datas[i+count][0])
    Phase_A[i]=float(datas[i+count][1])
    Phase_B[i]=float(datas[i+count][2])
    Voltage[i]=float(datas[i+count][3])
    

"""echo canceler """
p=200
A = np.zeros(rl,dtype = np.float) 
B = np.zeros(rl,dtype = np.float) 
for i in range(rl):
    if i+p < rl: 
        B[i] = Phase_B[i+p]-Phase_B[i]
        A[i] = Phase_A[i+p]-Phase_A[i]
order = 6
fs = 1200.0       # sample rate, Hz
cutoff = 60#3.667  # desired cutoff frequency of the filter, Hz

# Get the filter coefficients so we can check its frequency response.
b, a = butter_lowpass(cutoff, fs, order)
yA1 = butter_lowpass_filter(A, cutoff, fs, order)
yB1 = butter_lowpass_filter(B, cutoff, fs, order)
my_dpi=96
i = 0
while (i < rl):
    
    point ,time, delta = survey_event(i, yB1, rl,700)
    #print("test")
    if point != 0:   
        plt.figure(figsize=(18,5),num='startmeter') 
        
        plt.title('File:'+str(filenum)+', Data Record Time :' + str(time) +', start='+ str(point) +', len=10060')
        plt.plot(Voltage[point-1200:point+delta:1]/250,yB1[point-1200 :point+delta:1],color='r',label="B Cutoff 60Hz")
        plt.show()
        
        
        
        
        plt.figure(figsize=(18,5),num='startmeter') 
        
        plt.plot(Voltage[point-60:point+delta:1]/250,yB1[point-60 :point+delta:1],color='r',label="B Cutoff 60Hz")
        plt.title('File:'+str(filenum)+', Data Record Time :' + str(time) +', start='+ str(point) +', len=' + str(delta))
        #plt.figure(figsize=(800/my_dpi, 800/my_dpi), dpi=my_dpi)
        #plt.savefig('my_fig.png', dpi=my_dpi)
        plt.show()
        print(time)
        point = 0
        i += delta
    else:
        i += 1
#http://sci-hub.io 

#plt.plot(Voltage/250,yA1,color='b',label="B Cutoff 60Hz")

