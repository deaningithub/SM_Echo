# -*- coding: utf-8 -*-
"""
Created on Wed May  9 19:05:01 2018

@author: user
"""
import csv
#with open('some.csv', 'rb') as f:
#    reader = csv.reader(f)
#    for row in reader:
#        print row
def FileReadIn(f_EventListA ,Mode):
    with open(f_EventListA, Mode) as fo_EventListA:
        cin = csv.reader(fo_EventListA)
        data = [row for row in cin]
        return data
def FileReadInHeader(f_EventListA, line, Mode):
    data = []
    counter = 0
    with open(f_EventListA, Mode) as fo_EventListA:
        cin = csv.reader(fo_EventListA)
        for row in cin:
            data.append(row)
            counter += 1
            if counter == line:    
                break
        return data
def FileOpen(f_EventListA ,Mode):
    with open(f_EventListA, Mode) as fo_EventListA:
        cin = csv.reader(fo_EventListA)
        data = [row for row in cin]
        return data


