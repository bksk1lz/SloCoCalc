# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 17:01:04 2016

@author: bckin_000
"""
from points import *
from slocos import *

[namelistm, namelistw, racenumlist] = get_points()

namelistm.pop(0)
namelistw.pop(0)   

#Meetdirector Bonuses!
mds = open('MeetDirectors.txt', 'r')
mdsList = mds.read().split('\n')
mds.close()


for i, md in enumerate(mdsList):
    for dct in namelistm:
        if md in dct['name']:
            dct[racenumlist[i+1]] = sorted(dct.itervalues(), reverse = True)[1]
            
for i, md in enumerate(mdsList):
    for dct in namelistw:
        if md in dct['name']:
            dct[racenumlist[i+1]] = sorted(dct.itervalues(), reverse = True)[1]

racenumlist.append('best') 
racenumlist.append('SloCo') 
    
[allnames, allslocos] = get_slocos()

#number of races to count plus 1
SeasonSize = 9

#Men's and women's dictionaries now full of everybody's names and points for each race
#we need to get their best *SeasonSize* scores
from operator import itemgetter
             
for entry in namelistm:
    bestm = dict(sorted(entry.iteritems(), key = itemgetter(1), reverse = True)[1:SeasonSize])
    # sorts all dictionary values into a list. The text entry (person's name) is first
    # the best *SeasonSize* points values are 1 - 12 in the list. they are stored in the dictionary
    # bestm
    entry['best'] = sum(bestm.itervalues())
    #sum of the 11 best entries is added to each runners dictionary under the entry "sumbest11"
    try:
        entry['SloCo'] = allslocos[allnames.index(entry['name'])]    
    except ValueError:
        entry['SloCo'] = 0
#Now do the same thing for women's
for entry in namelistw:
    bestw = dict(sorted(entry.iteritems(), key = itemgetter(1), reverse = True)[1:SeasonSize])
    entry['best'] = sum(bestw.itervalues())
    entry['SloCo'] = allslocos[allnames.index(entry['name'])]
        

import csv
#write output .csv file.
#men's and women's dicts are just written consecutively for now
#would like to write this direct to google drive someday!
outfile = open("output.csv", "w")
w = csv.DictWriter(outfile, fieldnames = racenumlist, 
                   restval=0, extrasaction='ignore', dialect='excel')

for entry in namelistm:
    w.writerow(entry)
for entry in namelistw:
    w.writerow(entry)
outfile.close()
