# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 19:35:43 2018

@author: user
"""
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
def ThInit(i, y, length) :
    th = np.mean(np.absolute(y[i:i+length]))
    return th*10

""" Survey event """
def survey_event(start, y, length, nl, th):
    for i in range(start,length,1):
        # threshold should be tuned to find the best
        
        if np.absolute(y[i]) > th:
            if np.mean(y[i+10:i+60]) > th : #0.7 is tuned.
                 #Must modify!!!
                if start > nl*2:
                    noise = np.mean(np.absolute(y[i-nl*2:i-nl:1]))
                elif start > nl:
                    noise = np.mean(np.absolute(y[i-nl:i-nl//10:1]))
                else:
                    noise = np.mean(np.absolute(y[start:i:1]))
                event = np.mean(np.absolute(y[i:i+600:1]))
                if noise < 0.1:
                    noise = 0.1
                #print(event,noise,start)    
                for j in range(i+6000,length-600, 1):
                    end = np.mean(np.absolute(np.array(y[j:j+1200:1])))
                    #print(end,noise,j,i)
                    if end < noise*0.8+event*0.2: 
                        time = time_at_point(dataformat,X_value[i])
                        delta = j-i
                        #print(th)
                        #print('in if 1  ' + str(delta))
                        return i, time, delta
                   
              
        elif i == length-1:
            return -1, 0, i
        elif i > start+600:
            #print('jump!')
            return -2, 0, 800
        
def ComfirmFromEvenList(EventList, start, Len_el,time):
    Miss = []
    for i in range(start,Len_el):
        EventTime = datetime.strptime(EventList[i][0][0:23],EventList_FORMAT)
        TimeGap = EventTime - time
        print(time)
        GapSecond = TimeGap.total_seconds()
        if(np.absolute(GapSecond) < 0.1): # Time gap should less than 0.1 second. This value should be tuned.
           return 1,EventList[i][1],i+1,Miss
        elif GapSecond <0:
            Miss.append(EventList[i][0])
            print(EventList[i])
        elif GapSecond >0.1:
            Miss.append("Not List!, Time = "+str(time))
            #print("No flunt")
            return 0,"Nofound", i, Miss
        #else:
        #    return 0, "Error comfirm from event list", 0,Miss
            #print(TimeGap.total_seconds(),EventList[i][0][0:10])
    #for i in range()
    #print(Miss)
    
    #return 0,"Nofind",0,Miss
"""Example to get specify data time   
 
delaytime=0
delta = dataformat + timedelta(seconds = X_valueSe[delaytime], microseconds=X_valueMi[delaytime])
print(X_valueSe[delaytime],X_valueMi[delaytime])
print(datas[16][1],delta)
"""
import time
import csv
from datetime import datetime
from datetime import timedelta
import numpy as np
from scipy import fftpack
from scipy.signal import butter, lfilter, freqz
import matplotlib.pyplot as plt
import os

import time

start = time.time()

'''code you want to time goes here'''



Gename = "LoopSurveyLog6"
fo = open("D:\Idean\Smart meter\\"+Gename+".txt", "w")
fo_Miss = open("D:\Idean\Smart meter\\"+Gename+"Miss.txt", "w")
DATETIME_FORMAT = "%Y-%m-%d_%H:%M:%S.%f"
EventList_FORMAT = "%m/%d/%Y %H:%M:%S.%f"
#fo_EvenList = open("D:\Idean\Smart meter\location_001_dataset_001\location_001_eventslist.txt", "rt")
EventCountA = 1 # Start From 1.

with open("D:\Idean\Smart meter\location_001_dataset_001\location_001_eventslist_A.txt", "rt") as fo_EventListA:
    cin = csv.reader(fo_EventListA)
    EventListA = [row for row in cin]
Len_elA = len(EventListA) # legnth of EventList  

EventCountB = 1 # Start From 1.
with open("D:\Idean\Smart meter\location_001_dataset_001\location_001_eventslist_B.txt", "rt") as fo_EventListB:
    cin = csv.reader(fo_EventListB)
    EventListB = [row for row in cin]
Len_elB = len(EventListB) # legnth of EventList 


File_start =1
File_stop = 400
thresholdA = 0.15
thresholdB = 0.5 
#print(EvenList[Len_el-1])
for fin in range(File_start,File_stop):
    filenum=fin#248
    filepath="D:\Idean\Smart meter\location_001_dataset_001\location_001_ivdata_"+ '%03d' % fin+".txt"
    with open(filepath,'rt') as fileobj:
        cin = csv.reader(fileobj)
        datas = [row for row in cin]
    
    #11:58:32.6234999999996440291
    dataTime,microsecond=datas[10][1].split(".")
    microsecond = microsecond[0:6]  
    
    dataformat = datetime.strptime('2011-10-20_'+dataTime+'.'+microsecond,DATETIME_FORMAT)
    #print(dataTime)
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
        
    print("File "+str(filenum)+" at time "+str(time_at_point(dataformat,X_value[0])))
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
    
    if File_start - fin == 0:
        i = 0
        while (i < rl):
            point ,time, delta = survey_event(i, yA1, i+2400, 600, thresholdA)
            if point == -1 or point == -2:
                thresholdA = ThInit(i , yA1, 1200) 
                #print("Init th A")
                break
            i += 1
        
        i = 0
        while (i < rl):
            point ,time, delta = survey_event(i, yB1, i+2400, 600, thresholdB)
            if point == -1 or point == -2:
                thresholdB = ThInit(i , yB1, 1200) 
                print("Init th B "+str(thresholdB))
                break
            i += 1 
            
            i = 0
   
    # Find phase A event
    i = 0
    while (i < rl):
        
        point ,time, delta = survey_event(i, yA1, rl, 1200, thresholdA)
        
        #print("test")
        if point == -1:
            break
            
        elif point == -2:
            i += delta
            
        elif point > 0:
            #print(datetime.fromtimestamp(time).strftime("%Y-%m-%d_%H:%M:%S.%f"))
            
            '''
            plt.figure(figsize=(18,5),num='startmeter') 
            
            plt.title('File:'+str(filenum)+', Data Record Time :' + str(time) +', start='+ str(point) +', len=10060')
            plt.plot(Voltage[point-1200:point+delta:1]/250,yB1[point-1200 :point+delta:1],color='r',label="B Cutoff 60Hz")
            plt.show()
            
            '''
            #print(time.year)
           
            
            Answer,AppType, EventCountA, MissA = ComfirmFromEvenList(EventListA, EventCountA,Len_elA,time)
            #print("time = " + str(time.time()) + str(time.date()))
            #time = str(time) 
            #Big,Little = time.split(" ")
            #BL,ML,LL = Little.split(":") 
            #print(Big,Little,time.split(" ")[1])            
            print(Answer,AppType,EventCountA)
            #plt.figure(figsize=(18,5),num='startmeter') 
            PngDir_path = "D:\Idean\Smart meter\\"+Gename + "location_001_dataset_001_png\\"+ AppType
            if not os.path.exists(PngDir_path):
                os.makedirs(PngDir_path)
            
           # Save figure area 
            plt.figure(figsize=(800/my_dpi, 800/my_dpi), dpi=my_dpi)
            
            plt.plot(Voltage[point-600:point+delta:1]/250,yA1[point-600 :point+delta:1],color='r',label="B Cutoff 60Hz")
            plt.title('File:'+str(filenum)+', Data Record Time :' + str(time) +', start='+ str(point) +', len=' + str(delta)+", Phase A")
            PngPath = PngDir_path + "\\" + str(time.date())+"_"+str(time.hour).zfill(2)+"_"+str(time.minute).zfill(2)+"_"+str(time.second).zfill(2)+"."+str(time.microsecond)+".png"
            plt.savefig(PngPath, dpi=my_dpi)
            #----------------------------------------
            
            fo.write( str(time) + ',A ,start at ' +str(i)+' delta = '+str(delta) +', '+str(filenum)+", Phase A, Th ="+str(thresholdA)+'\n')
            fo_Miss.write( str(MissA)+'\n')

            i += delta
            point ,time, delta = survey_event(i, yA1, i+2400, 1200, thresholdA)
            if point == -1 or point == -2:
                if i+1200 < rl:
                    th = ThInit(i , yA1, 1200)
                    #print("get new th = " + str(th))
                    if th < 0.7:
                        thresholdA = th
                        #print(th)
                    else:
                        thresholdA = 0.7
                        #print(th)
                            
                     
                   
    # Find phase B event    
    i = 0    
    while (i < rl):
        point ,time, delta = survey_event(i, yB1, rl, 1200, thresholdB)
        #print("test")
        if point == -1:
            break
            
        elif point == -2:
            i += delta
            
        elif point > 0: 
            #time = str(time)
            '''
            plt.figure(figsize=(18,5),num='startmeter') 
            
            plt.title('File:'+str(filenum)+', Data Record Time :' + str(time) +', start='+ str(point) +', len=10060')
            plt.plot(Voltage[point-1200:point+delta:1]/250,yB1[point-1200 :point+delta:1],color='r',label="B Cutoff 60Hz")
            plt.show()
            
            '''
           
            Answer,AppType, EventCountB, MissB = ComfirmFromEvenList(EventListB, EventCountB,Len_elB,time)
            PngDir_path = "D:\Idean\Smart meter\\"+Gename + "location_001_dataset_001_png\\"+ AppType
            if not os.path.exists(PngDir_path):
                os.makedirs(PngDir_path)
                
            
            
           
            plt.figure(figsize=(800/my_dpi, 800/my_dpi), dpi=my_dpi)
            plt.plot(Voltage[point-600:point+delta:1]/250,yB1[point-600 :point+delta:1],color='r',label="B Cutoff 60Hz")
            plt.title('File:'+str(filenum)+', Data Record Time :' + str(time) +', start='+ str(point) +', len=' + str(delta)+", Phase B")
            PngPath = PngDir_path + "\\" + str(time.date())+"_"+str(time.hour).zfill(2)+"_"+str(time.minute).zfill(2)+"_"+str(time.second).zfill(2)+"."+str(time.microsecond)+".png"
            plt.savefig(PngPath, dpi=my_dpi)
            #print(Big)
            #plt.savefig(datetime.strptime('2011-11-20_'+time+'.'+microsecond,DATETIME_FORMAT)+".png", dpi=my_dpi)
            #plt.show()
            
            #print(threshold)
            #print(str(time) + ',B')
            fo.write( str(time) + ',B ,start at ' +str(i)+' delta = '+str(delta) +', '+str(filenum)+", Phase B, Th ="+str(thresholdB)+'\n')
            fo_Miss.write( str(MissB)+'\n')
            i += delta
            point ,time, delta = survey_event(i, yB1, i+2400, 1200, thresholdB)
            if point == -1 or point == -2:
                if i+1200 < rl:
                    th = ThInit(i , yB1, 1200)
                    if th < 2.5:
                        thresholdB = th 
                    else:
                        thresholdB = 2.5
                        #print(th)
fo.close()
fo_Miss.close() 

end = time.time()
elapsed = end - start
print("Time taken: ", elapsed, "seconds.")      
#http://sci-hub.io 

#plt.plot(Voltage/250,yA1,color='b',label="B Cutoff 60Hz")


