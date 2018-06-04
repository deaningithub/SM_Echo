# -*- coding: utf-8 -*-
"""
Created on Sat May 19 13:06:22 2018

@author: user
"""

import Module
import numpy as np
from numpy import genfromtxt
from datetime import datetime
from datetime import timedelta
import matplotlib.pyplot as plt
import time as tt




InputSinalFolder = "location_001_dataset_001"
File_start =14
File_stop = 15 # net 52
Gename = InputSinalFolder + "_LoopSurveyLog11"  # set the uniqe output file name
OutputTxtName = "E:\LoopSurveyOutput\\"+Gename+".txt"
OutputMissTxtName = "E:\LoopSurveyOutput\\"+Gename+"Miss.txt"
f_EventListA = "G:\SmartMeter\\" + InputSinalFolder + "\\location_001_eventslist_A.txt"
f_EventListB = "G:\SmartMeter\\" + InputSinalFolder + "\\location_001_eventslist_B.txt"
SignalFile = "G:\SmartMeter\\" + InputSinalFolder + "\\location_001_ivdata_"
PngDir = "E:\LoopSurveyOutput\\"
PngDir_Location =  InputSinalFolder + "_png\\"

DATETIME_FORMAT = "%Y-%m-%d_%H:%M:%S.%f"
EventList_FORMAT = "%m/%d/%Y %H:%M:%S.%f"



EventListA = FileReadIn(f_EventListA , "rt")        
EventListB = FileReadIn(f_EventListB, "rt")
Len_elA = len(EventListA)
Len_elB = len(EventListB)
EventCountA = 1
EventCountB = 1
EventRecordA = np.zeros(Len_elA,dtype = "b") 
EventRecordB = np.zeros(Len_elB,dtype = "b") 
CthFloor = 0.14
GthFloor = 0.1
gapFloor = 48000
OutCth = [0,CthFloor,CthFloor]
InerCth = [0,CthFloor,CthFloor]
Gth = [0,GthFloor,GthFloor]
thth = 0.3
Gain_check = [0,0,0]
Delta = [0,0,0]
G_delta= [0,0,0]

for fin in range(File_start,File_stop):
    S_position = 0
    
    fo = open(OutputTxtName, "a")
    fo_Miss = open(OutputMissTxtName, "a")
    filenum=fin#248
    filepath=SignalFile + '%03d' % fin + ".txt"
    ProcessFile =FileReadInHeader(filepath,23,'rt')
    count=23
    my_data = genfromtxt(filepath, delimiter=',',usecols=np.arange(0,4), invalid_raise = False,skip_header=23 )
    rl=len(my_data)
    print("rl="+str(rl))
    dateTime,microsecond=ProcessFile[10][1].split(".");    microsecond = microsecond[0:6]  
    
    TimeInit = datetime.strptime('2011-10-20_'+dateTime+'.'+microsecond,DATETIME_FORMAT)
    print(fin,time_at_point(TimeInit,my_data[1,0]))
    
    plt.ioff()
    start = tt.time()
    for phase in range(1,3):
        S_position = 0
        while S_position  < rl :
            Period= FindPeriod(S_position, my_data[:,phase],190,210,gapFloor,400)
            
            '''
            plt.figure(figsize=(10,5),num='CDelta') 
            plt.plot(my_data[S_position:S_position+200,0],my_data[S_position+gapFloor-Period:S_position+gapFloor-Period+200,phase],color='g',label="Period check data")
            plt.plot(my_data[S_position:S_position+200,0],my_data[S_position:S_position+200,phase],color='y',label="row Curve Delta")
            plt.plot(my_data[S_position:S_position+200,0],my_data[S_position:S_position+200,phase] - my_data[S_position+gapFloor-Period:S_position+200+gapFloor-Period,phase],color='r',label="p Curve Delta")
            plt.plot(my_data[S_position:S_position+200,0],my_data[S_position:S_position+200,phase] - my_data[S_position+gapFloor:S_position+200+gapFloor,phase],color='b',label="or Curve Delta")
            
            legend = plt.legend(loc='best', shadow=True, fontsize='x-large')#ax.arrow(X_value[503999], -10, X_value[503999], A[503999], head_width=0.05, head_length=0.1, fc='g', ec='g')
            plt.title('start at '+str(S_position))
            plt.show()
            '''
            S_position += 12000
    