#Title:         iota/Trigger.py
#Desc:          File to hold the Trigger Class and related Functions
#               The Function of the Trigger Class is to Recieve information from devices and activate a schedule from it.
#
#Last Update:   2024-2-20
#Updated By:    Blade Eastham
#Interpreter:   Python 3.11

##IMPORTS##
import json
from server import app

#CLASS DEFINITION#
class Trigger:
    ##VALUES##
    #id         Holds the id to store the Trigger in the database
    #data       Holds the data that is needed to set off the trigger
    #schedule   Holds the schedule that is activated when the trigger goes off
    #debug      Enables print statements for debugging purpose

    ##CONSTRUCTOR##
    def __init__(self, id:str, ScheduleID:str, data:dict[str, list[str]],  debug:bool=False):
        self.id = id
        self.data = data
        self.ScheduleID = ScheduleID
        self.debug = debug

def loadFromDatabase(id:str):
    cursor = app.config['cursor']
    connection= app.config['connection']

    query = ("SELECT * FROM triggers "
                "WHERE TriggerID = %s")
    cursor.execute(query, (id,))
    trigger = cursor.fetchone()
    if(trigger!=None):
        ScheduleID = trigger['ScheduleID']
        query = ("SELECT * FROM trigger_data "
                    "WHERE TriggerID = %s")
        cursor.execute(query, (id,))
        nextLine = cursor.fetchone()
        data = {}
        while(nextLine != None):
            data[nextLine['DeviceID']] = nextLine['Data']
            nextLine = cursor.fetchone()
        return Trigger(id=trigger['TriggerID'], data=data, ScheduleID=ScheduleID)
    else:
        return None

def checkTriggers():
    pass