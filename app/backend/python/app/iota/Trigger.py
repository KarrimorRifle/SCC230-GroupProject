#Title:         iota/Trigger.py
#Desc:          File to hold the Trigger Class and related Functions
#               The Function of the Trigger Class is to Recieve information from devices and activate a schedule from it.
#
#Last Update:   2024-2-18
#Updated By:    Blade Eastham
#Interpreter:   Python 3.11

##IMPORTS##
import json
from iota.Device import Device
from iota.Schedule import Schedule

#CLASS DEFINITION#
class Trigger:
    ##VALUES##
    #id         Holds the id to store the Trigger in the database
    #data       Holds the data that is needed to set off the trigger
    #schedule   Holds the schedule that is activated when the trigger goes off
    #debug      Enables print statements for debugging purpose

    ##CONSTRUCTOR##
    def __init__(self, id:str, data:dict[Device, list[str]]={}, ScheduleIDs:list[str]=[], debug:bool=False):
        self.id = id
        self.data = data
        self.scheduleIDs = scheduleIDs
        self.debug = debug

def loadFromDatabase(id:str):
    cursor = current_app.config['cursor']
    connection= current_app.config['connection']
    query = ("SELECT ScheduleID FROM schedules"
                "WHERE TriggerID = %s")
    cursor.execute(query, (id,))
    ScheduleIDs = cursor.fetchall()
    query = ("SELECT * FROM triggers "
                "WHERE TriggerID = %s")

    cursor.execute(query, (id,))
    Trigger = cursor.fetchone()

    #data parsing here
    #I don't know the format

    return Trigger(str(Trigger['TriggerID']), Trigger['Data'], ScheduleIDs)

def checkTriggers():
    pass