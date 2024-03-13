#Title:         iota/Trigger.py
#Desc:          File to hold the Trigger Class and related Functions
#               The Function of the Trigger Class is to Recieve information from devices and activate a schedule from it.
#
#Last Update:   2024-3-13
#Updated By:    Kian Tomkins
#Interpreter:   Python 3.11

##IMPORTS##
from server import app, addToErrorLog
import threading
from iota.Device import *
from iota.Schedule import *

#CLASS DEFINITION#
class Trigger:
    ##VALUES##
    #id         Holds the id to store the Trigger in the database
    #data       Holds the data that is needed to set off the trigger
    #devices    Holds a list of devices that the Trigger references
    #ScheduleID Holds the ID for the schedule that is activated when the trigger goes off
    #canRun     Whether or not a Trigger can or cannot activate it's linked schedule. 
    #debug      Enables print statements for debugging purpose

    ##CONSTRUCTOR##
    def __init__(self, id:str, ScheduleID:str, data:list[str],
                 canRun:bool=False, debug:bool=False):
        self.debug = debug
        self.id = id
        
        self.devices = []
        self.data = []
        for string in data:
            self.data.append(self.__resolveDatapoint(string))
        
        self.ScheduleID = ScheduleID
        self.canRun = canRun

        if(debug):
            print(f"Trigger Created With Values:\n"
                  f"id:\t\t{self.id}\n"
                  f"isRunning:\t{self.isRunning}\n"
                  f"ScheduleID:\t{self.ScheduleID}\n"
                  f"canRun:\t\t{self.canRun}\n"
                  f"devices:\t{str(self.devices)[:77]}...\n"
                  f"data:\t\t{str(self.data)[:77]}...\n")

    ##PUBLIC METHODS##
    #Updates the canRun value of a Trigger in the database
    def updateCanRun(self):
        cursor = app.config['cursor']
        query = ("UPDATE triggers"
                f"SET canRun = {1 if(self.canRun) else 0}"
                f"WHERE TriggerID = '{self.id}'")
        cursor.execute(query)

        if(self.debug):
            print(f"({self.id})\t Updated canRun to {self.canRun} in database")

    ##PRIVATE METHODS##
    #Formats the data into an evaluable string
    def __resolveDatapoint(self, datapoint:str):
        datapoint=str(datapoint)

        #Checks if the datapoint is an empty string
        if(len(datapoint) == 0):
            return '""'
        #Checks if the datapoint is a valid number
        try:
            _d = float(datapoint)
            return datapoint
        except:
            #Checks if the datapoint is referencing a string
            if('.' in datapoint):
                sDatapoint = datapoint.split(".")
                #Checks if it is a device in the database
                device=loadDeviceFromDatabase(sDatapoint[0])
                if(device != None):
                    #Adds device to the list of devices
                    if(device not in self.devices):
                        self.devices.append(device)
                        #Returns the formatted string
                        return f'self.devices[{len(self.devices)-1}].data["{sDatapoint[1]}"]'
                    else:
                        #Finds which device in self.devices the trigger uses
                        for i in range(len(self.devices)):
                            if(device == self.devices[i]):
                                #Returns the formatted string
                                return f'self.devices[{i}].data["{sDatapoint[1]}"]'
                    
        operators = ['<', '>', '<=', '>=', '==', '!=', # logical operators
                     'True', 'False', # boolean values
                     'AND', 'OR'] # logical extensions

        #Checks if the datapoint is an operator
        if(datapoint not in operators):
            #Checks if the variable is already in quotations
            if(datapoint[0] == '"' or datapoint[0] == "'"):
                datapoint[0] = ""
            if(datapoint[-1] == '"' or datapoint[-1] == "'"):
                datapoint[-1] = "" 
        #returns the string
        return str(datapoint)

##FUNCTION DEFINITIONS##
#Loads a Trigger from the database
def loadTriggerFromDatabase(id:str):
    cursor = app.config['cursor']

    query = ("SELECT TriggerID, ScheduleID FROM triggers "
                "WHERE TriggerID = %s")
    cursor.execute(query, (id,))
    trigger = cursor.fetchone()
    if(trigger!=None):
        ScheduleID = trigger['ScheduleID']
        query = ("SELECT Data, ListPos FROM trigger_data "
                    "WHERE TriggerID = %s")
        cursor.execute(query, (id,))
        triggerData = cursor.fetchall()
        triggerData = [row for row in triggerData]
        triggerData = sorted(triggerData, key=lambda x: x['ListPos'])

        data = []
        for row in triggerData:
            data.append(row['Data'])

        return Trigger(id=trigger['TriggerID'], data=data, ScheduleID=ScheduleID)
    else:
        return None

#Gets the IDs of all the triggers in database
def getTriggerIDs() -> list[str]:
    cursor = app.config['cursor']
    query = ("SELECT TriggerID FROM triggers")
    cursor.execute(query)
    return cursor.fetchall()

#Creates a semaphore to make sure all threads have been checked before checking them again
checkTriggersSemaphore = threading.Semaphore()

#Checks if any Triggers meet their data requirement 
def checkTriggers(ids:list[str]):
    #Checks an individual trigger in a new thread
    def checkATrigger(id):
        with(checkTriggersSemaphore):
            #Gets all the data about the trigger
            trigger=loadTriggerFromDatabase(id)

            #Checks the trigger exists
            if(trigger != None):
                #Updates the data in all the devices that the trigger uses 
                for device in trigger.devices:
                    device.updateData()

                #Checks if the code should run
                if(eval(' '.join(trigger.data))):
                    if(trigger.canRun):
                        #Runs the code
                        schedule = loadScheduleFromDatabase(trigger.ScheduleID)
                        if(trigger.debug):
                            print(f"({trigger.id}) running Schedule '{trigger.ScheduleID}'")
                        schedule.runCode()

                    #Stops the trigger from running multiple times from one activation
                    trigger.canRun = False
                else:
                    #Allows the trigger to run again
                    trigger.canRun = True
                #Updates the value of canRun in the database
                trigger.updateCanRun()
            else:
                addToErrorLog(f"Trigger '{id}' Does not exist.")

    threads = []
    #Checks the ID of each thread
    for trigger in ids:
        thread = threading.Thread(target=checkATrigger, args=(trigger,))
        thread.start()
        threads.append(thread)    
    
    #Joins the threads to stop checkTriggers from running again straight away
    for thread in threads:
        thread.join()

#Continually checks Triggers.
def main():
    try:
        while(True):
            checkTriggers(getTriggerIDs())
    #Prevents exit from python trying to close infinite loop
    except:
        main()

#running app
if __name__ == "__main__":
    app.run(debug=True, port=5000)
    main()