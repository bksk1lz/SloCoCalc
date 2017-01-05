def get_points():
    import os
    filelist = [] #Initialize list of files in directory
    
    #Get a list of all .xml files in directory
    for file in os.listdir(os.getcwd()):
        if file.endswith(".xml"):
            filelist.append(file)
    
    
    #This is an awkward way of building the list of point values to awards to each runner
    #1st value in the list is points for 1st place and so on
    pointslist = [100, 90, 81, 73, 66, 60, 55, 51, 47, 44, 41, 39, 37, 36, 35, 34,
                  33, 32, 31, 30, 29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18,
                  17, 16]
    pointslist2 = [15] * 65
    pointslist.extend(pointslist2)
    pointslist.append(5)
    pointslist.reverse()
    
    
    
    #From here on we are doing mens and womens results in parallel
    namelistm = [{}] #Initialize dictionary list of men's names and race results
    namelistw = [{}] ##Initialize dictionary list of women's names and race results
    
    #Get the list of women names
    #women.txt has a woman runner's name on each line
    #It is read into a list of the name strings
    women = open('women.txt', 'r')
    womenlist = women.read().split('\n')
    women.close()
    
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
        
        #Reinitialize points list for men and women ever time thru this loop because we 
        #pop off values to write points into namelist
        pointslistm = list(pointslist)
        pointslistw = list(pointslist)
        
        #take only the first class result in file. (sometimes there's a reverse course or something at the end)
        for ClassResult in root.find("ClassResult"):
            #Now we're in a loop iterating through the person results
            for PersonResult in ClassResult.iter("PersonResult"):
                namestr = ""
                x = 0 # A variable to keep track of whether the runner's name already exists in namelist
    
                #Write the runners name to namestr
                for Given in PersonResult.iter("Given"):
                    namestr = namestr + Given.text + " "
                                
                for Family in PersonResult.iter("Family"):
                    namestr = namestr + Family.text 
                    
                #Write resultposition to rpos
                for ResultPosition in PersonResult.iter("ResultPosition"):
                    rpos = ResultPosition.text
                         
                #Fist check women list to see if runner is a woman.
                if namestr in womenlist:
                    
                    for entry in namelistw:
                    
                        #iterate thru namelist for prior entry with the same name
                        if namestr in entry.values(): #if there is one, add raceposval to the dictionary
                            #pop from pointslistw to get points value because results file lists
                            #runners in finishing order
                            entry[racenumstr] = pointslistw.pop()
                            #if the runner mispunched, they were still rewarded the next poins in pointslistw
                            #but we need to give them 10. So check rpos, which will be None if runner MP
                            if rpos is None:
                                entry[racenumstr] = 10
                            x = 1
                        
                    if x == 0:
                        #if not, append namelist with a new entry, including name and race position
                        namelistw.append({"name":namestr, 
                                    racenumstr:pointslistw.pop()})
                        #do MP check again
                        if rpos is None:
                                entry[racenumstr] = 10
                    
                #if not a woman, do the same thing but in namelistm
                else:
                    for entry in namelistm:
                    
                        if namestr in entry.values(): 
                            entry[racenumstr] = pointslistm.pop()
                            if rpos is None:
                                entry[racenumstr] = 10
                            x = 1
                        
                    if x == 0:
                        namelistm.append({"name":namestr, 
                                    racenumstr:pointslistm.pop()})
                        if rpos is None:
                                entry[racenumstr] = 10
                
                #have to reset ResultPosition and rpos, otherwise old values will still be there and
                #the MP points won't get written
                ResultPosition.clear()
                rpos = None
                
   
    ''' 
    #Men's and women's dictionaries now full of everybody's names and points for each race
    #we need to get their best 11 scores
    from operator import itemgetter
                
    for entry in namelistm:
        best11m = dict(sorted(entry.iteritems(), key = itemgetter(1), reverse = True)[1:12])
        # sorts all dictionary values into a list. The text entry (person's name) is first
        # the best 11 points values are 1 - 12 in the list. they are stored in the dictionary
        # best10
        entry['best11'] = sum(best11m.itervalues())
        #sum of the 11 best entries is added to each runners dictionary under the entry "sumbest11"
        #entry['SloCo'] = allslocos[allnames.index(entry.name)]
    
    #Now do the same thing for women's
    for entry in namelistw:
        best11w = dict(sorted(entry.iteritems(), key = itemgetter(1), reverse = True)[1:12])
        entry['best11'] = sum(best11w.itervalues())
        
    

    #adds the sumbest11 entry title to racenumlist for inclusion in csv output
    #csv header is not working right now for some reason'''

    return [namelistm, namelistw, racenumlist]