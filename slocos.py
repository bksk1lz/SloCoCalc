
def get_sec(s):
    '''Returns time in seconds for string input, s, of form HH:MM:SS '''
    l = s.split(':')
    if len(l) == 1:
        return int(l[0])
    elif len(l) == 2:
        return int(int(l[0]) * 60 + int(l[1]))
    else:
        return int(int(l[0]) * 3600 + int(l[1]) * 60 + int(l[2]))


def get_slocos(filelist):

    # Men and women all go in one list since were handicapping absolute times
    namelist = [{}]  # Initialize dictionary list of names and race times

    # Now we are ready to go through the results files and write everyone's point values
    # to their entry in namelist
    import xml.etree.ElementTree as ET
    racenumlist = ["name"]

    # Load each file and make string for the race number
    for i, file in enumerate(filelist):
        tree = ET.parse(file)
        root = tree.getroot()
        racenumstr = "race" + str(i + 1)
        # builds a list of strings corresponding to the sequence of races
        racenumlist.append(racenumstr)

        # take only the first class result in file. (sometimes there's a
        # reverse course or something at the end)
        for ClassResult in root.find("ClassResult"):
            # Now we're in a loop iterating through the person results
            for PersonResult in ClassResult.iter("PersonResult"):

                for ResultPosition in PersonResult.iter('ResultPosition'):
                    rpos = ResultPosition.text

                if rpos is None:
                    break

                namestr = ""
                x = 0  # A variable to keep track of whether the runner's name already exists in namelist

                # Write the runners name to namestr
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
                    namelist.append({"name": namestr,
                                     racenumstr: timeval})

                Time.clear()
                timeval = None
                ResultPosition.clear()
                rpos = None

    racenumlist.pop(0)
    namelist.pop(0)

    for i, key in enumerate(racenumlist):
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
        orderedslocos = sorted(
            [v for v in entry.values() if isinstance(v, float)])
        midpoint = int(len(orderedslocos) / 2)

        if not len(orderedslocos) % 2:
            entry['SloCo'] = sum(
                orderedslocos[(midpoint - 1):(midpoint + 1)]) / 2
        else:
            entry['SloCo'] = orderedslocos[midpoint]
        allnames.append(entry['name'])
        allslocos.append(entry['SloCo'])
    return [allnames, allslocos]
