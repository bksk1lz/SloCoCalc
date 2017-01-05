
def get_sec(s):
    l = s.split(':')
    if len(l) == 1:
        return int(l[0])
    elif len(l) == 2:
        return int(int(l[0]) * 60 + int(l[1]))
    else:
        return int(int(l[0]) * 3600 + int(l[1]) * 60 + int(l[2]))
def get_slocos():
    import os
    filelist = [] #Initialize list of files in directory
    
    #Get a list of all .xml files in directory
    for file in os.listdir(os.getcwd()):
        if file.endswith(".xml"):
            filelist.append(file)
    
    
    
    #From here on we are doing mens and womens results in parallel
    namelist = [{}] #Initialize dictionary list of names and race times
    
    
    #Now we are ready to go through the results files and write everyone's point values
    #to their entry in namelist
    import xml.etree.ElementTree as ET
    racenumlist = ["name"]
    
    # Load each file and make string for the race number
    for i, file in enumerate(filelist):
        tree = ET.parse(file)
        root = tree.getroot()
        racenumstr = "race" + str(i+1)
        racenumlist.append(racenumstr)#builds a list of strings corresponding to the sequence of races
        
        #take only the first class result in file. (sometimes there's a reverse course or something at the end)
        for ClassResult in root.find("ClassResult"):
            #Now we're in a loop iterating through the person results
            for PersonResult in ClassResult.iter("PersonResult"):
                
                for ResultPosition in PersonResult.iter('ResultPosition'):
                    rpos = ResultPosition.text
                    
                if rpos is None:
                    break
                
                namestr = ""
                x = 0 # A variable to keep track of whether the runner's name already exists in namelist
    
                #Write the runners name to namestr
                for Given in PersonResult.iter("Given"):
                    namestr = namestr + Given.text + " "
                                
                for Family in PersonResult.iter("Family"):
                    namestr = namestr + Family.text 
    
                for Time in PersonResult.findall("./Result/Time"):
                    timestr = Time.text
                    timeval = get_sec(timestr)
                    break
                         
                for entry in namelist:
                    
                    if namestr in entry.values(): 
                        entry[racenumstr] = timeval
                        x = 1
                        
                if x == 0:
                    namelist.append({"name":namestr, 
                                    racenumstr:timeval})
    
                Time.clear()
                timeval = None
                ResultPosition.clear()
                rpos = None            
    
    racenumlist.pop(0)
    namelist.pop(0)
    
    
    for i,key in enumerate(racenumlist):
        racetimeslist = []
        for entry in namelist:
            if key in entry:
                racetimeslist.append(entry[key])
        
        wintime = float(min(racetimeslist))
        
        for entry in namelist:
            if key in entry:
                newkey = 'SloCo{0}'.format(i)
                entry[key] = float(entry[key]) / wintime
        
    
    
    allnames = []
    allslocos = []
                
    for entry in namelist:
        best11 = sorted(entry.values(), reverse = True)[1:18]
    
        midpoint = int(len(best11)/2)
        
        if not len(best11) % 2:
            entry['SloCo'] = sum(best11[(midpoint - 1):(midpoint + 1)]) / 2
        else:
            entry['SloCo'] = best11[midpoint]
        allnames.append(entry['name'])
        allslocos.append(entry['SloCo'])
    return [allnames, allslocos]
'''
#Now do the same thing for women's
for entry in namelistw:
    best11w = dict(sorted(entry.iteritems(), key = itemgetter(1), reverse = True)[1:12])
    entry['sumbest11'] = sum(best11w.itervalues())
    

racenumlist.append('sumbest11') 
#adds the sumbest11 entry title to racenumlist for inclusion in csv output
#csv header is not working right now for some reason

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
'''