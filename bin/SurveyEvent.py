import time as tt
import csv
from datetime import datetime
from datetime import timedelta
import numpy as np
from numpy import genfromtxt
#from scipy import fftpack
from scipy.signal import butter, lfilter, freqz
import matplotlib.pyplot as plt
import os
import sys
import Module


InputSinalFolder = "location_001_dataset_001"
File_start =1
File_stop = 401  # net 52
Gename = InputSinalFolder + "_LoopSurveyLog11"  # set the uniqe output file name
OutputTxtName = "E:\LoopSurveyOutput\\"+Gename+".txt"
OutputTxtName2 = "E:\LoopSurveyOutput\\"+Gename+"2.txt"

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
GthFloor = 0.15
gapFloor = 12000
OutCth = [0,CthFloor,CthFloor]
InerCth = [0,CthFloor,CthFloor]
Gth = [0,GthFloor,GthFloor]
thth = 0.3
Gain_check = [0,0,0]
Delta = [0,0,0]
G_delta= [0,0,0]
plt.ioff()
start = tt.time()

TP_A = 0 
FP_A = 0
FN_A = 0
#NOTN
P_A = 0 
N_A = 0
yti_A = 0
ytip_A = 0
ytb_A = 0

TP_B = 0 
FP_B = 0
FN_B = 0
#NOTN
P_B = 0 
N_B = 0
yti_B = 0
ytip_B = 0
ytb_B = 0

'''
Recall = TP/(TP + FN)
Precision = TP/(TP + FP)
F1 = 2 * (Precision * Recall) / (Recall + Precision)
Accuracy = (TP + TN) / (P + N)
'''

for fin in range(File_start,File_stop):
    S_position = 0
    
    fo = open(OutputTxtName, "a")
    
    filenum=fin#248
    filepath=SignalFile + '%03d' % fin + ".txt"
    ProcessFile =FileReadInHeader(filepath,23,'rt')
    count=23
    my_data = genfromtxt(filepath, delimiter=',',usecols=np.arange(0,4), invalid_raise = False,skip_header=23 )
    rl=len(my_data)
    print("rl="+str(rl))
    #Time setting
    dateTime,microsecond=ProcessFile[10][1].split(".");    microsecond = microsecond[0:6]  
    
    TimeInit = datetime.strptime('2011-10-20_'+dateTime+'.'+microsecond,DATETIME_FORMAT)
    print(fin,time_at_point(TimeInit,my_data[1,0]))
    

    #In Phase A
    for phase in range(1,3):
        print("====================\n In phase ",phase," \n====================")
        S_position = 0
        while S_position  < rl :
            Period= FindPeriod(S_position, my_data[:,phase],190,210,gapFloor,400)
            if Period == -1 or Period == -2:
                break
            Gain_check[phase] = 0
            Delta[phase], newCth, newS= SurveyCurveChange(S_position,rl,my_data[:,phase],my_data[:,0],gapFloor-Period,200,OutCth[phase],thth)
            S_position = newS+np.int(gapFloor/3*2)
                
            if Delta[phase] >= 0:
                
                print("Find Curve Change at ",Delta[phase],time_at_point(TimeInit,my_data[Delta[phase],0]),"to ")
                Period= FindPeriod(Delta[phase], my_data[:,phase],1,210,gapFloor,400)
                TempDelta, newCth, newS= SurveyCurveChange(Delta[phase],Delta[phase]+gapFloor,my_data[:,phase],my_data[:,0],gapFloor-Period,200,OutCth[phase],thth)
                S_position = newS+np.int(gapFloor/3*2)
                0.14
                if newCth == -2:
                    pass
                elif newCth > CthFloor:
                    OutCth[phase] = CthFloor
                        
                elif newCth < CthFloor:
                        OutCth[phase] = newCth*1.1
                        
                
                
                if TempDelta >= 0:
                    Delta[phase] = TempDelta 
                    print("Recheck success at Delta = ",Delta[phase])
                    
                    G_delta[phase], newGth = SurveyGainChange(Delta[phase],Delta[phase]+gapFloor,my_data[:,phase],gapFloor,2400,Gth[phase],rl) # 0.6 is gain diff, this value should be exp and cause the system sensitivity.
                    if newGth == -2:
                        pass
                    elif newGth < 0.3 :
                        if newGth < GthFloor:
                            Gth[phase] = GthFloor
                        else:
                            Gth[phase] = newGth
                    else:
                        Gth[phase] = 0.3
                    
                    print("Gth="+str(Gth[phase])+" G_Delta="+str(G_delta[phase]))
                    if G_delta[phase] == -2:
                        print("Gain Delta don't have enough gap between start-end\n auto break")
                        break
                    if np.absolute(G_delta[phase]) < Gth[phase]:
                            print("Got curve change but power, GDelta=",G_delta[phase]," Gth=",Gth[phase]," Cth=",OutCth[phase]," newCth=",newCth)
                            
                        #S_position = newS+12000
                    else:
                        print("Find curve change and power, GDelta=",G_delta[phase]," Gth=",Gth[phase]," Cth=",OutCth[phase]," newCth=",newCth)
                        
                        Gain_check[phase] = 1
                        #S_position = newS+12000
                    
                elif TempDelta == -2:
                    print("Got period error and recover!at ",S_position)
                
                
                
            elif Delta[phase] == -2:
                if S_position < rl:
                    print("Not found any curve change from \n",time_at_point(TimeInit,my_data[S_position,0])," to ",time_at_point(TimeInit,my_data[-1,0]))
                else:
                    print("Not found any curve change from \n",time_at_point(TimeInit,my_data[S_position-12000,0])," to ",time_at_point(TimeInit,my_data[-1,0]))
                #S_position = newS+12000
                break 
            if Delta[phase] == -1:
                print("In the file end, Auto break!")
                break
            
            if Gain_check[phase]:
                print("===============Find Event==============")
                time = time_at_point(TimeInit,my_data[Delta[phase],0])
                print("time row="+str(time)+"  Delta="+str(Delta[phase]))
            
                print("Gth=",Gth)
                if Delta[phase]+gapFloor < rl:
                    print(rl)
                    print(OutCth[phase])
                    PC,newCth,newS= SurveyCurveChange(Delta[phase],Delta[phase]+gapFloor,my_data[:,phase],my_data[:,0],200,200,InerCth[phase],thth)
                    S_position = newS+np.int(gapFloor/3*2)
                    #PC,newCth= FindPrecise(Delta,12000,my_data[:,phase],my_data[:,0],200,Cth)
                    print("PC="+str(PC))
                    
                else:
                    PC,newCth,newS= SurveyCurveChange(Delta[phase],rl,my_data[:,phase],my_data[:,0],200,200,InerCth[phase],thth)
                    S_position = newS+np.int(gapFloor/3*2)
                    print("In the file end")
                    
                if newCth == -2:
                    pass
                elif newCth < CthFloor:
                        InerCth[phase] = newCth*1.1
                elif newCth > CthFloor:
                        InerCth[phase] = CthFloor
    
            
    
                if PC == -2:
                    print("A Curve and Gain do change but can't find precise position!")
                    '''
                    plt.figure(figsize=(10,5),num='Delta') 
                    plt.plot(my_data[Delta[phase]:Delta[phase]+6000,3],my_data[Delta[phase]:Delta[phase]+6000,phase],color='k',label="First Curve")
                   
                    legend = plt.legend(loc='best', shadow=True, fontsize='x-large')#ax.arrow(X_value[503999], -10, X_value[503999], A[503999], head_width=0.05, head_length=0.1, fc='g', ec='g')
                    plt.title('PC start at '+str(Delta[phase]))
                    plt.show()
                    '''
                elif np.absolute(G_delta[phase]) > Gth[phase]:
                    time = time_at_point(TimeInit,my_data[PC,0])
                    print("time pre="+str(time)+"  Delta="+str(PC))
                    plt.figure(figsize=(10,5),num='CDelta') 
                    plt.plot(my_data[PC:PC+3000,3],my_data[PC:PC+3000,phase]-my_data[PC+200:PC+3000+200,phase],color='k',label="First Curve")
                   
                    legend = plt.legend(loc='best', shadow=True, fontsize='x-large')#ax.arrow(X_value[503999], -10, X_value[503999], A[503999], head_width=0.05, head_length=0.1, fc='g', ec='g')
                    plt.title('PC start at '+str(PC))
                    plt.show()
                    #tt.sleep(50)
                    if phase == 1:
                        Answer,AppType, EventCountA, EventRecordA = ComfirmFromEvenList(EventListA, EventCountA, Len_elA, time, EventRecordA)
                        if Answer:
                            pass
                        else:
                            FP_A += 1
                    if phase == 2:
                        Answer,AppType, EventCountB, EventRecordB = ComfirmFromEvenList(EventListB, EventCountB, Len_elB, time, EventRecordB)
                        if Answer:
                            pass
                        else:
                            FP_B += 1



                    fo.write( str(time) + ',A ,start at ' +str(S_position)+', '+str(filenum)+ \
                             ", Phase "+str(phase) +" Th ="+str(OutCth[phase])+", "+"Event th ="+str(newCth) +"," +str(AppType)+'\n')
                else:
                    print("Phase ",phase,",Special event with no power change but curve does, G_delta=",G_delta[phase])
                    break 
            print("===============Continue survey Event==============")
            
            
            

           
            #print(time)
            #S_position = Delta[phase] + 12000
  


fo_Text2 = open(OutputTxtName2, "a")
fo_Miss = open(OutputMissTxtName, "a")

for i in range(1, Len_elA-1):
    if EventRecordA[i] == 1:
        fo_Text2.write(str(EventListA[i])+'\n')
        TP_A += 1
    else:
        fo_Miss.write( str(EventListA[i])+'\n')
        FN_A += 1
        
for i in range(1, Len_elB-1):
    if EventRecordB[i] == 1:
        fo_Text2.write(str(EventListB[i])+'\n')
        TP_B += 1
    else:
        fo_Miss.write( str(EventListB[i])+'\n')
        FN_B += 1
Recall_A = TP_A/(TP_A + FN_A)
Precision_A = TP_A/(TP_A + FP_A)
F1_A = 2 * (Precision_A * Recall_A) / (Recall_A + Precision_A)
fo_Text2.write("A : Recall = "+str(Recall_A) +"Precision = "+str(Precision_A)+"F1 = "+str(F1_A) +"\n") 

Recall_B = TP_B/(TP_B + FN_B)
Precision_B = TP_B/(TP_B + FP_B)
F1_B = 2 * (Precision_B * Recall_B) / (Recall_B + Precision_B)
fo_Text2.write("B : Recall = "+str(Recall_B) +"Precision = "+str(Precision_B)+"F1 = "+str(F1_B) +"\n") 
     
fo.close()
fo_Miss.close()
fo_Text2.close()
        
#fo.close()
#fo_Miss.close()        
end = tt.time()
elapsed = end - start       

print("Time taken: ", elapsed, "seconds.")