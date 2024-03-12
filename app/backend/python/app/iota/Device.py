#Title:         iota/Device.py
#Desc:          File to hold the Device Class and related Functions
#               The Function of the Device Class is to hold information about IOT Devices
#
#Last Update:   2024-3-10
#Updated By:    Kian Tomkins
#Interpreter:   Python 3.11

##IMPORTS##
from server import app
from iota import addToErrorLog
import tinytuya as tuya

#Sets up the cloud server needed to connect to tuya devices
TUYASERVER = tuya.Cloud("eu", "p7ev9udc4nspppngqs9j", "eade3788ef124f97a7db3f6f000616e0")

##CLASS DEFINITION##
class Device:
    ##VALUES##
    #id         Holds the ID for the Device to be stored in the Database
    #name       Holds the name that the user will see for the Device
    #ip         Holds the IP of the Device
    #key        Holds the local key of the Device to confirm it's being accessed consentually
    #version    Holds the API version that TinyTuya uses to communicate with the device
    #mappings   Maps the Datapoint's number to it's code, so that the value can be accessed by name.
    #data       Holds the data for the device in a dict.
    #debug      Enables print statements for debugging purpose

    ##CONSTRUCTOR##
    def __init__(self, id:str, name:str, ip:str, key:str="", version:float=0.0, 
                 company:str="Tuya", debug:bool=False):
        self.id = id
        self.name = name

        self.company = company
        self.ip = ip

        if(self.company == "Tuya"):
            self.key = key
            self.version = version
            self.mappings = self.getMappings()

        self.data = {}
        self.updateData()

        self.debug = debug
        
    ##PUBLIC METHODS##
    #Gets the mappings for Datapoint Codes to Datapoint IDs 
    def getMappings(self) -> dict[str,str]:
        #Configures the server to get the devices on the user's network
        TUYASERVER.apiDeviceID = self.id
        
        #Gets the Datapoints from the server
        dps = TUYASERVER.getdps(self.id)['result']['status']
        mappings = {}

        #Adds the datapoints to the mappings
        for datapoint in dps:
            mappings[datapoint['dp_id']] = str(datapoint['code'])

    #Checks the current data against an external data, and sends any differences
    def changeData(self, data:dict):
        if(data != self.data):
            for key in self.mappings.keys():
                if(data[key] != self.data[key]):
                    self.sendData(key, self.data[key])

    #Updates the Data stored in the class and database
    def updateData(self):
        #Checks what company the device is from
        match(self.company):
            #If it is a Tuya Device
            case "Tuya":
                #Creates the Device
                apiDevice = tuya.Device(self.id, self.ip, self.key, self.version)

                #Updates The Data
                apiDevice.updatedps(list(self.mappings.keys()))
                newVals = apiDevice.status()['dps']

                #Maps the data
                for key in newVals.keys():
                    self.data[self.mappings[key]] = newVals[key]
            case _:
                addToErrorLog(f"Invalid Company \"{self.company}\"")
                return {"Error":-1}

    #Sends data to a device
    def sendData(self, variable:str, value:any):
        #Checks what company the device is from
        match(self.company):
            #If it is a Tuya Device
            case "Tuya":
                apiDevice = tuya.Device(self.id, self.ip, self.key, self.version)
                #Gets the mapping
                for mapping in self.mappings.keys():
                    if(self.mappings[mapping] == variable or mapping == variable):
                        apiDevice.set_value(mapping, value, True)
            case _:
                addToErrorLog(f"Invalid Company \"{self.company}\"")
                return {"Error":-1}

#Loads a Device From the Database
def loadDeviceFromDatabase(id:str) -> Device:
    cursor = app.config['cursor']
    query = ("SELECT * FROM devices "
                "WHERE DeviceID = %s")

    cursor.execute(query, (id,))
    device = cursor.fetchone()
    if(device == None):
        return None

    return Device(device['DeviceID'], device['DeviceName'], device['DeviceType'], device['IpAddress'], device['HubID'])
