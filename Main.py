# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 18:48:13 2018

@author: user
"""
import csv
import sys
import numpy as np
from scipy import fftpack
from scipy.signal import butter, lfilter, freqz
import matplotlib.pyplot as plt
#file info
filenum=248
filepath="D:\Idean\Smart meter\location_001_dataset_001\location_001_ivdata_"+str(filenum)+".txt"
with open(filepath,'rt') as fileobj:
    cin = csv.reader(fileobj)
    datas = [row for row in cin]
#12:36:58.32349999999999991920571,1189223
#12:38:37.42349999999999991826312,
plt.figure(figsize=(18,7),num='startmeter') 
dataTime=datas[16][1]    
count=23#+6000*63+1200#*2+1200*100#+600 #as least 23
count =959808-600*40#-1200*2#-600#9#+6000*15#+500
#scale: 50k->4.18 100k->8.34 1M->83.4
if count < 23:
    #print('Pleas set the start value more than 22 (at least 23)' )
    sys.exit("Pleas set the start value more than 22 (at least 23)")
rl=len(datas)-count#
#rl =len(datas)-count-60000*18-2400*8
rl =1200*40

if rl+count >len(datas):
    sys.exit("Out of range -> datas lenth just 1249223")

'''
for i in range(25):
    print(datas[i])
'''
    


#scale: 1000->5period


X_value = np.arange(rl,dtype = np.float)
Phase_A = np.arange(rl,dtype = np.float)
Phase_B = np.arange(rl,dtype = np.float)
Voltage = np.arange(rl,dtype = np.float)
Power = np.arange(rl,dtype = np.float)
AutoPA = np.zeros(rl,dtype = np.float)
A = np.zeros(rl,dtype = np.float) 
B = np.zeros(rl,dtype = np.float) 
V = np.zeros(rl,dtype = np.float)
for i in range(rl):
    X_value[i]=float(datas[i+count][0])
    Phase_A[i]=float(datas[i+count][1])
    Phase_B[i]=float(datas[i+count][2])
    Voltage[i]=float(datas[i+count][3])
    Power[i]=Phase_B[i]*Voltage[i]
    

p=200
#AutoPA =  Phase_A  
scal1 = np.zeros(p)

for i in range(rl):
    if i+p < rl: 
        #V[i] = Voltage[i+p]-Voltage[i]
        B[i] = Phase_B[i+p]-Phase_B[i]
        A[i] = Phase_A[i+p]-Phase_A[i]
        #AutoPA[i] = A[i] * V[i]
'''
a = np.array([1.0, -1.947463016918843, 0.9555873701383931])
b = np.array([0.9833716591860479, -1.947463016918843, 0.9722157109523452])
y = signal.lfilter(b, a, A)
'''
#fs = 1200
def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

order = 6
fs = 1200.0       # sample rate, Hz
cutoff = 60#3.667  # desired cutoff frequency of the filter, Hz

# Get the filter coefficients so we can check its frequency response.
b, a = butter_lowpass(cutoff, fs, order)
yA1 = butter_lowpass_filter(A, cutoff, fs, order)
yB1 = butter_lowpass_filter(B, cutoff, fs, order)



#AA = fftpack.fft(A)
#freqs = fftpack.fftfreq(len(A)) * f_s




'''
def A_res (x):
  return x  >   and x % 3 == 0
print filter(nums_res, nums)
'''
    
'''
for i in range(rl):
    Total=0
    for pe in range(p):
         if i+pe < rl:
             Total = Total + (AutoPA[i+pe]-AutoPA[i])*(AutoPA[i+pe]-AutoPA[i])
             scal1[pe]=Total
    print(scal1.min())
'''   




   
'''
scal=np.zeros(rl,dtype = np.float)
for i in range(rl):
    if i+p < rl:
        scal[i] = AutoPA[i+p]-AutoPA[i]
        if scal[i]*scal[i] < 0.8:
            scal[i]=0
            
    
plt.plot(range(rl),scal)
'''
#plt.plot(X_value,Phase_A,color="r")

#print(scal.min(),np.where(scal ==1539.751589419884))
#i, = np.where(a == value)
'''   
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

 
  

        for av in range(10):
            P=P+Phase_A[i+av]
            V=V+Voltage[i+av]
        Pmean[i+1] = P/10
        Vmean[i+1] = V/10
       

   
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
#plt.plot(X_value,Phase_A,color="k")
#plt.plot(X_value,Pmean)
#plt.plot(X_value,AutoPA)

#plt.plot(X_value,Phase_A/10,color='k',label="Phase_A/10")
#plt.plot(X_value,Power/500,color='g',label="Power B")
#ax = plt.axes()


plt.plot(X_value,Phase_B,color='k',label="Phase_B")
#plt.plot(X_value,Voltage/250,color='b',label="Voltage/250")

#plt.plot(X_value,A,color='b',label="A")
plt.plot(X_value,yB1,color='r',label="B Cutoff "+str(cutoff))
#plt.plot(X_value,yA1,color='r',label="A Cutoff "+str(cutoff))
#plt.plot(X_value,B,color='b',label="B without filter")
#plt.plot(X_value,Power/480,color='k',label="Power B/500")
#plt.plot(X_value,B,color='r',label="B without filter")
#plt.plot(X_value,yB1,color='r',label="B Cutoff 60Hz")

#plt.plot(X_value,y2,color='r',label="Cutoff 60Hz")
#plt.plot(X_value,y3,color='k',label="Cutoff 100Hz")

font = {'family': 'serif',
        'color':  'yellow',
 #       'color':  'Black',
        'weight': 'normal',
        'size': 16,
        }
#plt.text(X_value[959808], 1, 'I   LCD Monitor 1', fontdict=font)
#plt.text(X_value[809208], 5.5, 'I  Hallway stairs light', fontdict=font)
#plt.text(X_value[952200], -6.5, 'I  Basement lights', fontdict=font)
#plt.text(X_value[1018608], 7, 'I  Basement Receiver/DVR/Blueray Player', fontdict=font)
#plt.text(X_value[1140000], -3, 'I  TV', fontdict=font)

#'best'
legend = plt.legend(loc='best', shadow=True, fontsize='x-large')#ax.arrow(X_value[503999], -10, X_value[503999], A[503999], head_width=0.05, head_length=0.1, fc='g', ec='g')
plt.title('File:'+str(filenum)+', Data Record Time :' + dataTime +', start='+ str(count) +', len=' + str(rl))
plt.show()

# To show the frequency domain figure
'''
fig, ax = plt.subplots()

ax.stem(freqs, np.abs(AA))
ax.set_xlabel('Frequency in Hertz [Hz]')
ax.set_ylabel('Frequency Domain (Spectrum) Magnitude')
ax.set_xlim(-f_s / 2, f_s / 2)
ax.set_ylim(-5, 110)'''
#plt.figure(figsize=(18,13),num='startmeter')
 
'''
#random wolk
plt.figure(figsize=(24,13),num='startmeter') 
#plt.plot(X_value,Phase_A)
plt.scatter(X_value,Power,s=1)
plt.show()
plt.figure(figsize=(24,13),num='startmeter')
plt.plot(X_value,Phase_A)
plt.show()
#keras-recurrent
'''
    #general [papar]