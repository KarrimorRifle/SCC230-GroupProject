#Title:         iota/Trigger.py
#Desc:          File to hold the Trigger Class and related Functions
#               The Function of the Trigger Class is to Recieve information from devices and activate a schedule from it.
#
#Last Update:   2024-3-11
#Updated By:    Kian Tomkins
#Interpreter:   Python 3.11

##IMPORTS##
from server import app
import threading
from iota.Device import Device
from iota.Schedule import *

#CLASS DEFINITION#
class Trigger:
    ##VALUES##
    #id         Holds the id to store the Trigger in the database
    #data       Holds the data that is needed to set off the trigger
    #schedule   Holds the schedule that is activated when the trigger goes off
    #debug      Enables print statements for debugging purpose

    ##CONSTRUCTOR##
    def __init__(self, id:str, ScheduleID:str, data:dict[str, list[str]], canRun:bool=False, debug:bool=False):
        self.id = id
        self.data = data
        self.ScheduleID = ScheduleID
        self.canRun = canRun
        self.debug = debug

    def updateCanRun(self):
        cursor = app.config['cursor']
        query = ("UPDATE triggers"
                f"SET canRun = {1 if(self.canRun) else 0}"
                f"WHERE TriggerID = {self.id}")

# Function creates Trigger object based on Trigger data in DB
def loadTriggerFromDatabase(id:str):
    cursor = app.config['cursor']

    query = ("SELECT TriggerID, ScheduleID FROM triggers "
                "WHERE TriggerID = %s")
    cursor.execute(query, (id,))
    trigger = cursor.fetchone()
    if(trigger!=None):
        ScheduleID = trigger['ScheduleID']
        query = ("SELECT DeviceID, Data, ListPos FROM trigger_data "
                    "WHERE TriggerID = %s")
        cursor.execute(query, (id,))
        triggerData = cursor.fetchall()
        triggerData = [row for row in triggerData]
        triggerData = sorted(triggerData, key=lambda x: x['ListPos'])

        data = {}
        for row in triggerData:
            if data.get(row['DeviceID']) is None:
                data[row['DeviceID']] = []
            
            data[row['DeviceID']].append(row['Data'])

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
            #Checks if the code should run
            if(eval(trigger.data)):
                if(Trigger.canRun):
                    schedule = loadScheduleFromDatabase(trigger.ScheduleID)
                    schedule.runCode()
                #Stops the trigger from running multiple times from one activation
                trigger.canRun = False
            else:
                #Allows the trigger to run again
                trigger.canRun = True
            #Updates the value of canRun in the database
            trigger.updateCanRun()

    threads = []
    #Checks the ID of each thread
    for trigger in ids:
        thread = threading.Thread(target=checkATrigger, args=(trigger,))
        thread.start()
        threads.append(thread)    
    
    #Joins the threads to stop checkTriggers from running again straight away
    for thread in threads:
        thread.join()

#continually checks Triggers.
def main():
    while(True):
        checkTriggers(getTriggerIDs())
