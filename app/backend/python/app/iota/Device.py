#Title:         iota/Device.py
#Desc:          File to hold the Device Class and related Functions
#               The Function of the Device Class is to hold information about IOT Devices
#
#Last Update:   2024-2-29
#Updated By:    Kian Tomkins
#Interpreter:   Python 3.11

##IMPORTS##
from server import app

##CLASS DEFINITION##
class Device:
    ##VALUES##
    #id         Holds the ID for the Device to be stored in the Database
    #name       Holds the name that the user will see for the Device
    #isActive   Checks if the Device is currently in use
    #data       Holds the data for the device in a dict.
    #debug      Enables print statements for debugging purpose

    ##CONSTRUCTOR##
    def __init__(self, id:str, name:str, deviceType:str, ipAddress:str, hubID:str, isActive:bool=False,
                 debug:bool=False):
        self.id = id
        self.name = name
        self.deviceType = deviceType
        self.ipAddress = ipAddress
        self.hubID = hubID
        self.isActive = isActive
        self.debug = debug
    
    #Updates the Data
    def updateData(self) -> dict[str, any]:
        pass

def loadFromDatabase(id:str) -> Device:
    cursor = app.config['cursor']
    query = ("SELECT * FROM devices "
                "WHERE DeviceID = %s")

    cursor.execute(query, (id,))
    device = cursor.fetchone()

    return Device(device['DeviceID'], device['DeviceName'], device['DeviceType'], device['IpAddress'], device['HubID'])
    pass