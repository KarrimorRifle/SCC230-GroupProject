#Title:         iota/Device.py
#Desc:          File to hold the Device Class and related Functions
#               The Function of the Device Class is to hold information about IOT Devices
#
#Last Update:   2024-1-18
#Updated By:    Kian Tomkins
#Interpreter:   Python 3.11

##IMPORTS##
from iota.Api import Api

##CLASS DEFINITION##
class Device:
    ##VALUES##
    #id         Holds the ID for the Device to be stored in the Database
    #name       Holds the name that the user will see for the Device
    #api        Holds the API that is attached to the device
    #isActive   Checks if the Device is currently in use

    ##CONSTRUCTOR##
    def __init__(self, id:str, name:str, api:Api=None, isActive:bool=False):
        self.id = id
        self.name = name
        self.api = api
        self.isActive = isActive