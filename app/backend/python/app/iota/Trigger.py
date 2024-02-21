#Title:         iota/Trigger.py
#Desc:          File to hold the Trigger Class and related Functions
#               The Function of the Trigger Class is to Recieve information from devices and activate a schedule from it.
#
#Last Update:   2024-2-21
#Updated By:    Aditya Khan
#Interpreter:   Python 3.11

##IMPORTS##
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


# Function creates Trigger object based on Trigger data in DB
def loadFromDatabase(id:str):
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

def checkTriggers():
    pass