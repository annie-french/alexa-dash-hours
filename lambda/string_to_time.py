import json
#this file opens filtered_output.txt and creates a list of lists with the following format:
#[[building name, type, open_known, openhr, openmin, opensec, close_known, closehr, closemin, closesec], ... ]

#determines if building is open or closed then calls the corresponding function
#input: raw_input
#output: list with the following values [open hour, close hour, open min, close min]]
def convert(raw_input):
    if raw_input.__contains__("appointment"):
        return [0,0,0,0]
    if raw_input[0]=="O":
        return openBuildingHandler(raw_input)
    else:
        return closedBuildingHandler(raw_input)

#handles cases where building is currently closed
#input: raw_input
#output: list with the following values [open hour, close hour, open min, close min]
def closedBuildingHandler(raw_input):
    open_minute, close_minute=find_minutes(raw_input, "closed")
    lst=raw_input.split(" ")
    if lst[2]!="today":
        return [0,0,0,0]
    else:
        lst = removeMinutes(lst)
        convertToTwentyFour(lst)
        openTime=findTimes(lst)
        
        #last two indices are minutes        
        return[openTime[0],0,open_minute,0]

#handles cases where building is currently open 
#input: raw_input
#output: list with the following values [open hour, close hour, open min, close min]             
def openBuildingHandler(raw_input):
    if raw_input.count("–")>1:
        return multiWindowHandler(raw_input)
    open_minute, close_minute=find_minutes(raw_input, "open")    
    no_dashes_input= remove_dash(raw_input)
    
    lst=no_dashes_input.split(" ")
    lst = removeMinutes(lst)
    lst=convertToTwentyFour(lst)
    times = findTimes(lst)
    times[0]=validate_open_hour(times[0])
    while len(times)<2:
        times.append(0)    
    #minutes
    times.append(open_minute)
    times.append(close_minute)

    return times

#handles cases where building is open for multiple windows of time during the day
#input: raw_input
#output: list with the following values [open hour, close hour, open min, close min] 
def multiWindowHandler(raw_input):
    open_minute, close_minute=find_minutes(raw_input, "multi")
    no_dashes_input= remove_dash(raw_input)
    lst=no_dashes_input.split(" ")
    lst = removeMinutes(lst)
    lst=convertToTwentyFour(lst)
    times = findTimes(lst)
    start_and_end=[]
    start_and_end.append(times[0])
    start_and_end.append(times[-1])
    
    #minutes
    start_and_end.append(open_minute)
    start_and_end.append(close_minute)
    #minutes

    return (start_and_end)

#input: raw_input and building type(closed, open, multi)
#output the minutes that the building opens and closes as integers
def find_minutes(raw_input, building_type):
    open_min, close_min = 0,0
    
    if building_type=="closed":
        for i in range(len(raw_input)):
            if raw_input[i]==":":
                minutes=raw_input[i+1:i+3]
                if minutes.isdigit():
                    open_min=int(minutes)
    
    if building_type=="open":
        dash_index=-1
        for i in range(len(raw_input)):
            if raw_input[i]=="–":
                dash_index=i        
        if dash_index>0:
            for i in range(len(raw_input)):
                if raw_input[i]==":":
                    minutes=raw_input[i+1:i+3]
                    if minutes.isdigit():
                        if i<dash_index:
                            open_min=minutes
                        if i>dash_index:
                            close_min=minutes

    if building_type=="multi": 
        for i in range(len(raw_input)):
            if raw_input[i]=="–":
                open_string=raw_input[0:i+1]
                break
        for i in range(len(raw_input)):
            if raw_input[i]=="–":
                close_string=raw_input[i:len(raw_input)+1]

        for i in range(len(open_string)):
            if open_string[i]==":":
                minutes=open_string[i+1:i+3]
                if minutes.isdigit():
                    open_min=minutes
        for i in range(len(close_string)):
            if close_string[i]==":":
                minutes=close_string[i+1:i+3]
                if minutes.isdigit():
                    close_min=minutes   
    return int(open_min), int(close_min) 
    
#some open times are listed without a p.m. distintion
#this function catches and fixes those cases
#input: open hour (int)
#output: open hour (int)
def validate_open_hour(open_hour):
    if open_hour==1 or open_hour==2:
        open_hour+=12
    return open_hour

#input: string list
#output: string list without a dash 
def remove_dash(input_list): 
    for i in range(len(input_list)):
        if input_list[i]=="–":
            input_list=input_list.replace("–", " ")
    return input_list

#input: string list: input
#output: string list: input without minutes
def removeMinutes(input_list):
    times_with_minutes=[]
    for i in range(len(input_list)):
        if input_list[i].__contains__(":"):
            times_with_minutes.append(i)                        
    for index in times_with_minutes:
        time=input_list[index]
        for j in range(len(time)):
            if time[j]==":":
                hour=time[0:j]
                input_list[index]=hour
    return input_list            

#input: string list: list of strings
#output: int list: list of indices of all integers in input
def findTimes(lst):
    times=[]
    for i in lst:
        if i.isdigit():
            times.append(int(i))    
    return times

#input: string list: list of strings
#output: string list: input list, but all times converted to military and all 
#        string representations of times are converted to numeric representations
def convertToTwentyFour(lst):
    stringTimes={"noon": "12", "midnight": "23"}#need to add minutes to 23
    for i in range(len(lst)):
        if lst[i] in stringTimes:
            lst[i]=(stringTimes[lst[i]])
        if lst[i]=="p.m.":
            lst[i-1]=str(int(lst[i-1])+12)
    return lst

#opens file and returns a list of lines in the file
def open_file():
    file1=open("filtered_output.txt", "r")
    lines=[]
    for line in file1:
        lines.append(line[0:-1])
    return lines

#input: html string from dash
#output: the approprtiate building type 
def find_type(raw_input):
    if raw_input.__contains__("appointment"):
        return "appointment"
    if raw_input.count("–")>1:
        return "interruptions"
    if raw_input[0]=="O":
        return "normal"
    else:
        return "closed"

#input: list of lists w/ buildings information
#output: dictionary w/ buildings information
def arraytoDic(buildingList):
    building_dic = {}
    for list in buildingList:
        individual_dic = {}
        building = list[0]
        type = list[1]
        open_known = list[2]
        open_hour = list[3]
        open_min = list[4]
        open_sec = list[5]
        close_known = list[6]
        close_hour = list[7]
        close_min = list[8]
        close_sec = list[9]

        individual_dic[building] = {}
        individual_dic[building]['type'] = type

        individual_dic[building]['open_dic'] = {}
        individual_dic[building]['open_dic']['openKnown'] = open_known
        individual_dic[building]['open_dic']['openHour'] = open_hour
        individual_dic[building]['open_dic']['openMin'] = open_min
        individual_dic[building]['open_dic']['openSec'] = open_sec
        
        individual_dic[building]['close_dic'] = {}
        individual_dic[building]['close_dic']['closeKnown'] = close_known
        individual_dic[building]['close_dic']['closeHour'] = close_hour
        individual_dic[building]['close_dic']['closeMin'] = close_min
        individual_dic[building]['close_dic']['closeSec'] = close_sec
                
        building_dic.update(individual_dic)

    return building_dic

#input: buildings dictionary
#output: Fills in build_info.json
def JsonCreate(building_dic):

    json_object = json.dumps(building_dic,indent=4)

    with open("build_info.json", "w") as outfile:
        outfile.write(json_object)
    
def main():
    lines=open_file()
    building_list=[]

    for i in range(1,len(lines),2):
        building_info=[]
        
        name=lines[i-1]
        building_info.append(name)
        
        building_type=find_type(lines[i])
        building_info.append(building_type)
      
        times=convert(lines[i])
        open_known="true"
        building_info.append(open_known)
       
        #open hr
        building_info.append(times[0])
        #minutes
        building_info.append(times[2])
        #seconds
        building_info.append(0)
        
        if times[1]==0 and times[0]!=0:
            close_known="false"
        else:
            close_known="true" 
        building_info.append(close_known)

        #close hr
        building_info.append(times[1])
        #minutes
        building_info.append(times[3])
        #seconds
        building_info.append(0) 
        
        building_list.append(building_info)
    #print(building_list)  

    dictionary = arraytoDic(building_list)
    JsonCreate(dictionary)
if __name__ == "__main__":
    main()
