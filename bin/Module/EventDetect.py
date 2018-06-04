# -*- coding: utf-8 -*-
"""
Created on Wed May  9 18:56:59 2018

@author: user
"""


def SurveyCurveChange(start, end, y, x, gap, length, th,thth):
    #print(th)
    i = start
    Fl_CDelta = 0
    temp_record=[]
    temp_record.append(0)
    if gap > 400:
        i_Delta = np.int(gap/2)
    else:
        i_Delta = gap
    if end - start < gap:
        print("Don't have enough gap between start-end")
        return -1,0,i
    while i+gap+length < end:
        
        CDelta = y[i:i+length]-y[i+gap:i+gap+length] # Curve Delta
        order = 6
        fs = 1200.0       # sample rate, Hz
        cutoff = 60#
       
        Fl_CDelta = butter_lowpass_filter(CDelta, cutoff, fs, order)
        
        #print(np.mean(SC),np.mean(EC))
        '''
        plt.figure(figsize=(10,5),num='CDelta') 
        plt.plot(x[i:i+length],y[i:i+length],color='k',label="First Curve")
        plt.plot(x[i:i+length],y[i+gap:i+gap+length],color='r',label="End Curve")
        plt.plot(x[i:i+length],CDelta,color='b',label="Curve Delta")
        
        legend = plt.legend(loc='best', shadow=True, fontsize='x-large')#ax.arrow(X_value[503999], -10, X_value[503999], A[503999], head_width=0.05, head_length=0.1, fc='g', ec='g')
        plt.title('i start at '+str(i))
        plt.show()
        print(np.mean(np.absolute(Fl_CDelta)),th)
        '''     
        #print(np.mean(np.absolute(Fl_CDelta)))
        temp_record.append(np.mean(np.absolute(Fl_CDelta)))
        if np.mean(np.absolute(Fl_CDelta)) > th:
            if i+gap*2 < end:
                newth =np.mean(np.absolute(y[i+gap-length:i+gap]-y[i+gap*2-length:i+gap*2]))
            else:
                newth =np.mean(np.absolute(y[i+gap-length:i+gap]-y[i+gap:i+gap+length]))
            '''
            plt.figure(figsize=(10,5),num='CDelta') 
            plt.plot(x[i:i+length],y[i:i+length],color='k',label="First Curve")
            plt.plot(x[i:i+length],y[i+gap:i+gap+length],color='r',label="End Curve")
            plt.plot(x[i:i+length],Fl_CDelta,color='b',label="Curve Delta")
            
            legend = plt.legend(loc='best', shadow=True, fontsize='x-large')#ax.arrow(X_value[503999], -10, X_value[503999], A[503999], head_width=0.05, head_length=0.1, fc='g', ec='g')
            plt.title('i start at '+str(i)+' newth='+str(newth))
            plt.show()
            print("value=",np.mean(np.absolute(Fl_CDelta))," th=",th)
            #newth = y[i+gap:i+gap+length]-y[i+gap+length:i+gap+length*2]
            '''
            print("In SurveyCurveChange, eventTH=",np.mean(np.absolute(Fl_CDelta)),",th=",th)
            return i,newth*1.5,i
        i+=i_Delta
    print("Can't find curve change, event th value=",max(temp_record)," th=",th)
            
    return -2,-2,i
#Period= FindPeriod(Delta, my_data[:,3],190,210,12000,400)
        
def FindPrecise(start, gap, y, x, length,Cth):
    print(start,start+gap,len(y))
    Period= FindPeriod(start, y,190,210,400,400) # Need to add
    print("Precise ="+str(Period))
    Delta,Cth= SurveyCurveChange(start,start+gap,y,x,length,length,Cth)
    print("new p ="+str(Delta))        
    
    return Delta,newCth
def SurveyGainChange(start, end, y, gap, length, th,rl):

    i = start
    if end - start < gap:
        print("Don't have enough gap between start-end")
        return -1,-1
    if end + gap + length > rl:
        print("Don't have enough gap between start-end")
        return -2,-2
    SC = np.absolute(y[i:i+length])#Start Current
    EC = np.absolute(y[i+gap:i+gap+length])
    G_delta = np.mean(SC- EC) 
    print("G_delta="+str(G_delta)," start=",start," end",end)
    while (i+gap+length < end):
        if G_delta > th:
            print(SC,EC,i)
        elif G_delta < -th:
            print(SC,EC,i)
        i += np.int(gap/2)
        SC = EC
        EC = np.absolute(y[i+gap:i+gap+length])
    #th = np.mean(y[start:end])
    newth =  np.absolute(np.mean(y[i+gap-length:i+gap] -y[i+gap:i+gap+length]))
    #print(SC,EC)
    return G_delta ,newth*3

def getmean(i, y, length) :
    th = np.mean(np.absolute(y[i:i+length]))
    return th*10
def getPowerMean(i, x, y, length) :    
    return np.mean(np.absolute(x[i:i+length] * y[i:i+length]))

""" Survey event """
def CheckEventFeature(start, y, Y, length, nl, th):
    for i in range(start,length,1):
        # threshold should be tuned to find the best

        if np.absolute(y[i]) > th:
            
            SGain = np.mean(y[i+10:i+60])
            if SGain > th : #0.7 is tuned.
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
                for j in range(i+1200,length-600, 1):
                    end = np.mean(np.absolute(np.array(y[j:j+1200:1])))
                    #print(end,noise,j,i)
                    if end < event*0.7: 
                        time = time_at_point(dataformat,X_value[i])
                        delta = j-i
                        return i, time, delta, SGain
                   
                else:
                     return -4, 0 , 800, SGain
        elif i == length-1:
            return -1, 0, i, 0
        elif i > start+600:
            #print('jump!')
            return -2, 0, 800, 0
    return -3, 0, length, 0
    
def survey_event(start, y, Y, length, nl, th):
    
    while start < length:
        
        SC = getmean(start, Y, 4800)
        EC = getmean(start+length, Y ,4800)
        #
        #
        if np.absolute(SC - EC) > 0.6:
            return -3, 0, length, 0
            #return CheckEventFeature(start, y, Y, length, nl, th)
        else:
            print(start)
            print(np.absolute(SC - EC))
            start += 6000
  
    print("OUt loop")   
    return -3, 0, length, 0
           


                
def ComfirmFromEvenList(EventList, start, Len_el,time, EventRecord):
    #print("In ComfirmFromEvenList")
    #print("time="+str(time))
    #print("EventList = "+str(EventList[start][0][0:23]))
    
    for i in range(start,Len_el):
        #print(Len_el,i,EventList[i][0][0:23])
        EventTime = datetime.strptime(EventList[i][0][0:23],EventList_FORMAT)

        TimeGap = EventTime - time
        #print(EventTime)
        GapSecond = TimeGap.total_seconds()
        #print("Time Gap = "+str(GapSecond))
        #mid = 0.8
        if(np.absolute(GapSecond) < 1.49) : # Time gap should less than 0.1 second. This value should be tuned.
           if EventRecord[i] == 1:
               print("Muti")
               return 1, "Muti-" +EventList[i][1], i, EventRecord
           else: 
               EventRecord[i] = 1
               print("Found")
               #print(EventRecord[i])
               return 1,EventList[i][1],i,EventRecord
           
        elif GapSecond >0.2:
            print("Nolist")
            return 0,"NoList", 1, EventRecord
    
    # If can't found in Eventlist, return nofound.
    return 0,"NoList", 1, EventRecord