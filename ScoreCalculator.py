# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 17:01:04 2016

@author: bckin_000
"""
import os
import csv
import points
import slocos

userpath = input('Enter path to results files: ')
filelist = sorted([userpath + file for file in os.listdir(userpath)
                   if file.endswith('.xml')])


SeasonSize = int(input('Enter the number of races to count: '))

women = open(userpath + '/women.txt', 'r')
womenlist = women.read().split('\n')
women.close()

[rposlistlist, racenumlist] = points.get_positions(filelist)

[rpll_men, rpll_women] = points.men_women(womenlist, rposlistlist)

namelistw = points.get_points(rpll_women)
namelistm = points.get_points(rpll_men)


namelistm.pop(0)
namelistw.pop(0)

# Meetdirector Bonuses!
mds = open(userpath + '/MeetDirectors.txt', 'r')
mdsList = mds.read().split('\n')
mds.close()


for i, md in enumerate(mdsList):
    for dct in namelistm:
        if md in dct['name']:
            try:
                dct[racenumlist[i + 1]] = sorted([v for v in dct.values()
                                                  if isinstance(v, int)],
                                                 reverse=True)[0]
            except:
                pass

for i, md in enumerate(mdsList):
    for dct in namelistw:
        if md in dct['name']:
            try:
                dct[racenumlist[i + 1]] = sorted([v for v in dct.values()
                                                  if isinstance(v, int)],
                                                 reverse=True)[0]
            except:
                pass

racenumlist[1:1] = ['best', 'SloCo']
print(namelistm)
print(racenumlist)

[allnames, allslocos] = slocos.get_slocos(filelist)

# Men's and women's dictionaries now full of everybody's names and points for
# each race we need to get their best *SeasonSize* scores
from operator import itemgetter

for entry in namelistm:
    bestm = sorted([v for v in entry.values() if isinstance(v, int)],
                   reverse=True)[0:SeasonSize]
    # sorts all dictionary values into a list. The text entry (person's name)
    # is first the best *SeasonSize* points values are 1 - 12 in the list
    entry['best'] = sum(bestm)
    # sum of the 11 best entries is added to each runners dictionary under the
    # entry "sumbest11"
    try:
        entry['SloCo'] = allslocos[allnames.index(entry['name'])]
    except ValueError:
        entry['SloCo'] = 0
# Now do the same thing for women's
for entry in namelistw:
    bestw = sorted([v for v in entry.values() if isinstance(v, int)],
                   reverse=True)[0:SeasonSize]
    entry['best'] = sum(bestw)
    try:
        entry['SloCo'] = allslocos[allnames.index(entry['name'])]
    except ValueError:
        entry['SloCo'] = 0


# write output .csv file.
# men's and women's dicts are just written consecutively for now
# would like to write this direct to google drive someday!
outfile = open(userpath + "output.csv", "w")
w = csv.DictWriter(outfile, fieldnames=racenumlist,
                   restval=0, extrasaction='ignore', dialect='excel')
x = csv.writer(outfile)

x.writerow(['Men\'s results'])
w.writeheader()
for entry in sorted(namelistm, key=itemgetter('best'), reverse=True):
    w.writerow(entry)
x.writerow(['Women\'s results'])
w.writeheader()
for entry in sorted(namelistw, key=itemgetter('best'), reverse=True):
    w.writerow(entry)
outfile.close()
