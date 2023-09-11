import datetime
import json

#Input: takes building string from Alexa slot values defined in en_US.json
#output: returns an integer value to lambda_function to indicate whether input
        # was found in buildings dictionary

def OpenOrClosed(building, curr_time):

    """
    current__dt format looks like: 2021-06-25 07:58:56.550604
    Type: Object
    building: building name as a string
    """
    all_buildings = {}
    with open('build_info.json') as json_file:
        data = json.load(json_file)
    '''
    for x in data:
        building = Building(x['name'], x['type'])
        building.set_open(x['open_dic']['openHour'], x['open_dic']['openMin'], x['open_dic']['openSec'])
        building.set_close(x['close_dic']['closeHour'], x['close_dic']['closeMin'], x['close_dic']['closeSec'])
        all_buildings[x['name']] = building
        
    '''

    data = {k.lower(): v for k, v in data.items()}
    """
    for i in data.keys():
        data.keys()[i] = data.keys()[i].lower()
        print(data.keys()[i])
        """
    #returns time instance in 07:58:56.550604 format
    #print(data.keys())
    #curr_time = datetime.datetime.now().time()


    if building in data.keys():
        start = datetime.time(data[building]['open_dic']['openHour'], data[building]['open_dic']['openMin'], data[building]['open_dic']['openSec'])
        end = datetime.time(data[building]['close_dic']['closeHour'], data[building]['close_dic']['closeMin'], data[building]['close_dic']['closeSec'])
        
        if curr_time > start and curr_time < end:
            return 1
        else:
            return 0 
    else:
        print("No such building found")
        return -1

def checkBuildHours(building):
    with open('build_info.json') as json_file:
        data = json.load(json_file)
    data = {k.lower(): v for k, v in data.items()}
    if building in data.keys():
        start = str(data[building]['open_dic']['openHour']) + ":" + str(data[building]['open_dic']['openMin'])
        end = str(data[building]['close_dic']['closeHour']) + ":" + str(data[building]['close_dic']['closeMin'])
        return start, end
    else:
        print("No such building found")
        return "-1", "-1"