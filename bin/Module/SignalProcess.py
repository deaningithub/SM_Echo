# -*- coding: utf-8 -*-
"""
Created on Fri May 11 10:52:12 2018

@author: user
"""

from scipy import signal


def FindPeriod(start, sig,R_max,R_min,gap,S_length):
    #print(start)
    if start + S_length+800 < len(sig):
        S_s = sig[start: start + S_length+800]
    else:
        print("S_s don't have enough length")
        return -2
    if start + gap + S_length < len(sig):
        E_s = sig[start + gap : start + gap + S_length]
    else:
        print("E_s don't have enough length")
        return -1
    #print(len(S_s),len(E_s))
    corr = signal.correlate(S_s, E_s, mode='same')
    #print(np.mean(np.absolute(S_s-E_s)))'
    
    RE_S_p = sig[start: start + S_length]-sig[start + gap-np.argmax(corr) : start + gap-np.argmax(corr) + S_length]
    #RE_S_d = sig[start: start + S_length]-sig[start + gap+np.argmax(corr) : start + gap+np.argmax(corr) + S_length]
    print(np.mean(np.absolute(E_s)),np.mean(np.absolute(RE_S_p)))
    if R_max == 1:
        '''
        plt.figure(figsize=(10,5),num='CDelta') 
        plt.plot(range(S_length),sig[start: start + S_length],color='k',label="Recheck First Curve")
        plt.plot(range(S_length),sig[start + gap-np.argmax(corr) : start + gap + S_length-np.argmax(corr)],color='r',label="Recheck End Curve")
        #plt.plot(range(len(corr)),corr,color='b',label="Curve Delta")
        #plt.plot(range(S_length),S_s-E_s,color='y',label="row Curve Delta")
        #plt.plot(range(S_length),RE_S_p,color='r',label="p Curve Delta")
        #plt.plot(range(S_length),RE_S_d,color='b',label="d Curve Delta")
        
        legend = plt.legend(loc='best', shadow=True, fontsize='x-large')#ax.arrow(X_value[503999], -10, X_value[503999], A[503999], head_width=0.05, head_length=0.1, fc='g', ec='g')
        plt.title('start at '+str(start))
        plt.show()
        '''
   
    print("corr max = ",np.argmax(corr))
    return np.argmax(corr)#-S_length