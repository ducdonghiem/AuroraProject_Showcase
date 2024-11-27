import class_optimization
import schedule_retrieve

def calculate_result(term, courses_list):
    
    classes_list, weirdCourses = schedule_retrieve.schedule_retrieve(term, courses_list)
    if isinstance(classes_list, str):
        error = classes_list
        ways, smallestTimeGap, best_class_list, printResult, startTime_list, endTime_list, class_list_ways, weirdCourses = "0"*8

    else: 
        error = "none"
        ways, smallestTimeGap, best_class_list, startTime_list, endTime_list, class_list_ways = class_optimization.main(classes_list, weirdCourses)

        printResult = "There are: " + str(ways) + " ways.\n Smallest time gap is " + str(smallestTimeGap) + " \nwith schedule: \n" + str(best_class_list) 

    return error, ways, smallestTimeGap, best_class_list, printResult, startTime_list, endTime_list, class_list_ways, weirdCourses

def calculate_customization(customized_class_list_ways, weekDay, dayTime, customTime):
    customized_class_list_ways, ways, smallestTimeGap, best_class_list, startTime_list, endTime_list = class_optimization.customization(customized_class_list_ways, weekDay, dayTime, customTime)
    return customized_class_list_ways, ways, smallestTimeGap, best_class_list, startTime_list, endTime_list
    