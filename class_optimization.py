def courseArangement(course):
    for i in range(7):
        return 0
    

# take in time and convert to numbers
def timeEncoder(time):
    # days = [i for i in time[1]]
    startTime = time[0:5]
    startPeriod = time[6:8]
    endTime = time[9:14]
    endPeriod = time[15:17]
    if startPeriod == "am":
        startTime = int(startTime[0:2]) + int(startTime[3:5])/60        # convert to real number
    if startPeriod == "pm":
        startTime = 12 + int(startTime[0:2])%12 + int(startTime[3:5])/60
    if endPeriod == "am":
        endTime = int(endTime[0:2]) + int(endTime[3:5])/60
    if endPeriod == "pm":
        endTime = 12 + int(endTime[0:2])%12 + int(endTime[3:5])/60

    return (startTime, endTime)


def backtracking(k, classes_list, class_list, class_list_ways, n):
    for key, value in classes_list[k].items():
        if checkEligibility(value, k, class_list):
            class_list[k] = {key: value}
            if k == n - 1:
                class_list_ways.append(class_list.copy())           
            else:
                backtracking(k+1, classes_list, class_list, class_list_ways, n)


# check eligibility for backtracking
def checkEligibility(value, k, class_list):
    if k == 0:
        return 1
    else:
        for i in range(k):
            temp_value = list(class_list[i].values())               
            for day in value[1]:                                   
                if day in temp_value[0][1]:                         
                    if checkOverlap(value[0], temp_value[0][0]):    
                        return 0             
    return 1

# check whether 2 times are overlap 
def checkOverlap(time1, time2):
    startTime1, endTime1 = timeEncoder(time1)
    startTime2, endTime2 = timeEncoder(time2)
    if (startTime1 <= startTime2 and startTime2 < endTime1) or (startTime2 <= startTime1 and startTime1 < endTime2):
        return 1
    return 0

# calculate and return time gap and the number of days having classes in a week of each option
def timeGapCalculation(class_list):
    timeGap = 0
    countDays = 0
    for day in "MTWRF":
        startTime_list = []
        endTime_list = []
        firstCountDay = True
        for i in range(len(class_list)):
            for key, value in class_list[i].items():
                if day in value[1]:
                    if firstCountDay:
                        countDays += 1
                        firstCountDay = False
                    startTime, endTime = timeEncoder(value[0])
                    startTime_list.append(startTime)
                    endTime_list.append(endTime)
        startTime_list.sort()
        endTime_list.sort()
        for j in range(1,len(startTime_list)):
            timeGap += startTime_list[j] - endTime_list[j-1]
                    
    return timeGap, countDays            


# find best option with the smallest time gap and number of class days of a classes list
def bestClassList(ways):
    smallestTimeGap = 1000
    smallestNumDays = 7
    best_class_list = []
    best_class_list_index = 0
    i = -1
    for _class_list in ways:
        i += 1
        timeGap, countDays = timeGapCalculation(_class_list)
        if countDays < smallestNumDays:
            best_class_list = _class_list.copy()
            smallestNumDays = countDays
            smallestTimeGap = timeGap
            best_class_list_index = i
        elif countDays == smallestNumDays:
            if timeGap < smallestTimeGap:
                smallestTimeGap = timeGap
                best_class_list = _class_list.copy()
                best_class_list_index = i
        # print(timeGap)
    
    startTime_list, endTime_list = startEndTimeList(best_class_list)                # will be used in frontend
    return smallestTimeGap, best_class_list, startTime_list, endTime_list, best_class_list_index

# return startTime_list and endTime_list of an option for drawing the table of that option
def startEndTimeList(class_list): 
    startTime_list = []                     # will be used in frontend
    endTime_list = []
    for i in range(len(class_list)):
        for key, value in class_list[i].items():
            startTime, endTime = timeEncoder(value[0])
            startTime_list.append(startTime)
            endTime_list.append(endTime)
    return startTime_list, endTime_list

# return all possible options, the smallest time gap as the best option
def main(classes_list, weirdCourses):
    
    n = len(classes_list)
    class_list = [0]*n
    class_list_ways  = []
    
    backtracking(0, classes_list, class_list, class_list_ways, n)       
   
    if len(weirdCourses) != 0:
        for weirdCourse in weirdCourses:
            for option in class_list_ways[:]:               
                section = ""
                isFirst = True
                remove = False
                for i in range(len(option)):       
                    for key, value in option[i].items():
                        if isFirst and key[0:-3] == weirdCourse and key[-3:-2] != "B":
                            section = key[-3:]
                            isFirst = False
                        if (not isFirst) and key[0:-3] == weirdCourse and key[-3:] != section and key[-3:-2] != "B":
                            class_list_ways.remove(option)
                            remove = True
                            break
                    if remove:
                        break

    smallestTimeGap, best_class_list, startTime_list, endTime_list, best_class_list_index = bestClassList(class_list_ways)
    if len(class_list_ways) > 0:
        class_list_ways[best_class_list_index] = class_list_ways[0].copy()
        class_list_ways[0] = best_class_list.copy()
    
    return (len(class_list_ways), "{:.2f}".format(smallestTimeGap), best_class_list, startTime_list, endTime_list, class_list_ways)


def customization(customized_class_list_ways, customizedDay, noclassTime, customTime):
    
    validIndexes = []
    timePeriod_dict = {"morning": "08:00 am-11:00 am", "midday": "11:00 am-01:00 pm", "afternoon": "01:00 pm-17:00 pm", "evening": "17:00 pm-22:00 pm"}

    if noclassTime == "customize":
        finalNoClassTime = customTime
    elif noclassTime != "allday":
        finalNoClassTime = timePeriod_dict[noclassTime]

    
    for i in range(len(customized_class_list_ways)):
        valid = 1
        for _class in customized_class_list_ways[i]:
            
            days = list(_class.values())[0][1]              
           
            if customizedDay in days:
                if noclassTime == "allday":
                    valid = 0
                    break
                else:
                   
                    if checkOverlap(finalNoClassTime, list(_class.values())[0][0]):
                        valid = 0
                        break
        if valid == 1:
            validIndexes.append(i)
      

    new_customized_class_list_ways = []
    for i in validIndexes:
        new_customized_class_list_ways.append(customized_class_list_ways[i].copy())
    
    customized_class_list_ways = new_customized_class_list_ways.copy()

    smallestTimeGap, best_class_list, startTime_list, endTime_list, best_class_list_index = bestClassList(customized_class_list_ways)

   
    if len(customized_class_list_ways) > 0:
        customized_class_list_ways[best_class_list_index] = customized_class_list_ways[0].copy()
        customized_class_list_ways[0] = best_class_list.copy()

    return (customized_class_list_ways, len(customized_class_list_ways), "{:.2f}".format(smallestTimeGap), best_class_list, startTime_list, endTime_list)
