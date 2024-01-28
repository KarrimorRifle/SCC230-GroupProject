#Title:         iota/Trigger.py
#Desc:          File to hold the Trigger Class and related Functions
#               The Function of the Trigger Class is to Recieve information from devices and activate a schedule from it.
#
#Last Update:   2024-1-27
#Updated By:    Kian Tomkins
#Interpreter:   Python 3.11

##IMPORTS##
import json
from iota.Device import Device

#CLASS DEFINITION#
class Trigger:
    ##VALUES##
    #id     Holds the id to store the Trigger in the database
    #data   Holds the data that is needed to set off the trigger
    #debug  Enables print statements for debugging purpose

    ##CONSTRUCTOR##
    def __init__(self, id:str, data:dict[Device, list[str]]={}, debug:bool=False):
        self.id = id
        self.data = data
        self.debug = debug