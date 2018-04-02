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
filepath="D:\Idean\Smart meter\location_001_dataset_001\location_001_ivdata_005.txt"
with open(filepath,'rt') as fileobj:
    cin = csv.reader(fileobj)
    datas = [row for row in cin]

plt.figure(figsize=(24,13),num='startmeter') 

count=23+5000*0 #as least 23
#scale: 50k->4.18 100k->8.34 1M->83.4
if count < 23:
    #print('Pleas set the start value more than 22 (at least 23)' )
    sys.exit("Pleas set the start value more than 22 (at least 23)")

rl=1200*75

#scale: 1000->5period

if rl+count >len(datas):
    sys.exit("Out of range -> datas lenth just 1249223")
X_value = np.arange(rl,dtype = np.float)
Phase_A = np.arange(rl,dtype = np.float)
Voltage = np.arange(rl,dtype = np.float)
for i in range(rl):
    X_value[i]=float(datas[i+count][0])
    Phase_A[i]=float(datas[i+count][1])
    Voltage[i]=float(datas[i+count][3])
    
i=0 
count=0
meanLen=20
Pmean=np.zeros(rl,dtype = np.float)
Vmean=np.zeros(rl,dtype = np.float)
P=0
V=0
Pmean[0]=Phase_A[0]
Pmean[1]=Phase_A[1]
getPeak_XOne=np.zeros(rl,dtype = np.float)
getPeak_XTwo=np.zeros(rl,dtype = np.float)
getPeak_XThr=np.zeros(rl,dtype = np.float)
getPeak_XFor=np.zeros(rl,dtype = np.float)
getPeak_One=np.zeros(rl,dtype = np.float)
getPeak_Two=np.zeros(rl,dtype = np.float)
getPeak_Thr=np.zeros(rl,dtype = np.float)
getPeak_For=np.zeros(rl,dtype = np.float)
mux=0
for i in range(Phase_A.size-meanLen):
    P=0
    V=0
    

    
    #print(X_value[i],(Pmean[i]-Phase_A[i+1])*(Phase_A[i+1]-Phase_A[i+2]))
    if mux==0:
        if (Pmean[i]-Phase_A[i+3])*(Phase_A[i+3]-Phase_A[i+6]) < -0.8:
            # getPeak_XOne[i+1]=X_value[i+1]
            getPeak_One[i+1]=Phase_A[i+1]
            Pmean[i+1] = Pmean[i]-Pmean[i-1]+Pmean[i]
            Vmean[i+1] = Vmean[i]-Vmean[i-1]+Vmean[i]
            mux=1
            #plt.text(X_value[i], Pmean[i+1],(Pmean[i]-Phase_A[i+3])*(Phase_A[i+3]-Phase_A[i+6]) , fontsize=20)
    
        elif (Pmean[i]-Phase_A[i+1])*(Phase_A[i+1]-Phase_A[i+2]) < -0.3:
            getPeak_Thr[i+1]=Phase_A[i+1]
            Pmean[i+1] = (Pmean[i]-Pmean[i-1])*0.6+Pmean[i]
            Vmean[i+1] = Vmean[i]-Vmean[i-1]+Vmean[i]
            mux=1
            #plt.text(X_value[i], Pmean[i+1],(Pmean[i]-Phase_A[i+1])*(Phase_A[i+1]-Phase_A[i+2]) , fontsize=20)
        else:
            Pmean[i+1]=Phase_A[i+1]
            Vmean[i+1]=Voltage[i+1]
            mux=0
    if mux==1:
        if (Pmean[i]-Phase_A[i+1])*(Pmean[i]-Phase_A[i+1]) >1:
            Pmean[i+1] = (Pmean[i]-Pmean[i-1])*0.6+Pmean[i]
            Vmean[i+1] = Vmean[i]-Vmean[i-1]+Vmean[i] 
            
        else:
            Pmean[i+1] = (Pmean[i]-Pmean[i-1])+Pmean[i]
            Vmean[i+1] = Vmean[i]-Vmean[i-1]+Vmean[i] 
            mux=0
 
   
       #Phase_A[i+3] =(Phase_A[i+1]*2+Pmean[i+1])/3

 
  
'''
        for av in range(10):
            P=P+Phase_A[i+av]
            V=V+Voltage[i+av]
        Pmean[i+1] = P/10
        Vmean[i+1] = V/10
'''        

'''   
for i in range(100):
    print(Pmean[i])
'''

#Power=np.multiply(Voltage, Phase_A)
'''
x=range(Pmean.size)
plt.figure(figsize=(24,13),num='startmeter') 
plt.plot(x,Pmean)
'''
#plt.show()

#plt.scatter(X_value,getPeak_One,s=40,color="g")
#plt.scatter(X_value,getPeak_Two,s=40,color="r")
#plt.scatter(X_value,getPeak_Thr,s=40,color="y")
#plt.scatter(X_value,getPeak_For,s=40,color="k")
#plt.plot(X_value,Phase_A,color="r")
plt.plot(X_value,Pmean)

plt.show()
'''
#random wolk
plt.figure(figsize=(24,13),num='startmeter') 
#plt.plot(X_value,Phase_A)
plt.scatter(X_value,Power,s=1)
plt.show()
plt.figure(figsize=(24,13),num='startmeter')
plt.plot(X_value,Phase_A)
plt.show()
'''
    #general [papar]