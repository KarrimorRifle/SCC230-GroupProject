#Title:         iota/Device.py
#Desc:          File to hold the Device Class and related Functions
#               The Function of the Device Class is to hold information about IOT Devices
#
#Last Update:   2024-3-13
#Updated By:    Kian Tomkins
#Interpreter:   Python 3.11

##IMPORTS##
from server import app, addToErrorLog
import tinytuya as tuya

#Sets up the cloud server needed to connect to tuya devices
TUYASERVER = tuya.Cloud("eu", "p7ev9udc4nspppngqs9j", "eade3788ef124f97a7db3f6f000616e0")

##CLASS DEFINITIONS##
class Device:
    ##VALUES##
    #id                 Holds the ID for the Device to be stored in the Database
    #name               Holds the name that the user will see for the Device
    #ip                 Holds the IP of the Device
    #key                Holds the local key of the Device to confirm it's being accessed consentually
    #version            Holds the API version that TinyTuya uses to communicate with the device
    #company            The company that the device is manufactured by
    #mappings           Maps the Datapoint's number to it's code, so that the value can be accessed by name.
    #typeMappingsIn     Maps the Datapoint's read-only variables to their Type, so that the values the user can send are restricted
    #typeMappingsOut    Maps the Datapoint's read-and-write variables to their Type, so that the values the user can send are restricted
    #data               Holds the data for the device in a dict.
    #debug              Enables print statements for debugging purpose

    ##CONSTRUCTOR##
    def __init__(self, id:str, name:str, ip:str, key:str="", version:float=0.0, 
                 company:str="Tuya", debug:bool=False):
        self.debug = debug
        self.id = id
        self.name = name

        self.company = company
        self.ip = ip
        self.data = {}

        if(self.company == "Tuya"):
            self.key = key
            self.version = version

            self.typeMappingsIn = {}
            self.typeMappingsOut = {}
            self.mappings = {}

            self.updateMappings()
            

        
        self.updateData()

        
        if(debug):
            print(f"Device Created With Values:\n"
                  f"id:\t\t\t{self.id}\n"
                  f"name:\t\t\t{self.name}\n"
                  f"company:\t\t{self.company}\n"
                  f"ip:\t\t\t{self.ip}\n"
                  f"key:\t\t\t{self.key}\n"
                  f"version:\t\t{self.version}\n"
                  f"typeMappingsIn:\t\t{str(self.typeMappingsIn)[:100]}...\n"
                  f"typeMappingsOut:\t{str(self.typeMappingsOut)[:100]}...\n"
                  f"mappings:\t\t{str(self.mappings)[:100]}...\n"
                  f"data:\t\t\t{str(self.data)[:100]}...\n")
        
    ##PUBLIC METHODS##
    #Gets the mappings for Datapoint Codes to Datapoint IDs 
    def updateMappings(self):
        if(self.debug):
            print(f"({self.id})\t Updating Mappings.")
    
        #Configures the server to get the devices on the user's network
        TUYASERVER.apiDeviceID = self.id
        
        #Gets the Datapoints from the server
        dps = TUYASERVER.getdps(self.id)['result']
        readables = dps['status'] 
        writeables = dps['functions']
        dps = readables + writeables

        #Adds the datapoints to the mappings
        query = ("INSERT INTO device_vars (DeviceID, VarName, VarType) "
                 "VALUES ")
        for datapoint in dps:
            #Changes Enums to strings, to be processed later
            if(datapoint['type'] == 'Enum'):
                datapoint['type'] = 'STRING'

            #Checks if the datapoint read-only
            if(datapoint not in writeables):
                self.typeMappingsIn[datapoint['code']] = datapoint['type'].upper()
            #Checks if the datapoint is not write-only
            elif(datapoint in readables):
                self.typeMappingsOut[datapoint['code']] = datapoint['type'].upper()
            self.mappings[datapoint['dp_id']] = datapoint['code']

            query += f"('{self.id}', '{datapoint['code']}', '{datapoint['type']}'),"
        
        #Updates the database with the new mappings
        try:
            query = query[:-1]
            cursor = app.config['cursor']
            cursor.execute(query)
            app.config['connection'].commit()
        except Exception as e:
            print(f"Error executing query: {e}")
            addToErrorLog(e)
                
    #Checks the current data against an external data, and sends any differences
    def changeData(self, oldData:dict[str, any]):
        #Checks if the full dataset is the same, to save time
        if(oldData != self.data):
            #Checks what has changed
            for key in self.mappings.keys():
                if(oldData[key] != self.data[key]):
                    if(self.debug):
                        print(f"({self.id})\t Updating {key} from '{oldData[key]}' to '{self.data[key]}'.")

                    #Completes the change
                    self.sendData(key, self.data[key])

    #Updates the Data stored in the class and database
    def updateData(self):
        #Checks what company the device is from
        match(self.company):
            #If it is a Tuya Device
            case "Tuya":
                #Creates the Device
                apiDevice = tuya.Device(dev_id=self.id, address=self.ip, local_key=self.key, version=self.version)

                #Updates The Data
                apiDevice.updatedps(index=list(self.mappings.keys()), nowait=True)
                newVals = apiDevice.status()
                #Checks Datapoints were retrieved
                try:
                    newVals = newVals['dps']
                except:
                    addToErrorLog(f"({self.id}) Couldn't retreive DPS. api.status() returned '{newVals}'")

                if(self.debug):
                    print(f"({self.id})\t Fetching the data stored on a Tuya {self.version} Device at {self.ip}.")

                #Maps the data
                for key in newVals.keys():
                    self.data[key] = newVals[key]
                    if(self.debug):
                        try:
                            print(f"({self.id})\t Data: {self.mappings[int(key)]} Set to {newVals[key]}")
                        except:
                            print(f"({self.id})\t Data: UNKNOWN Set to {newVals[key]}")
            case _:
                addToErrorLog(f"Invalid Company \"{self.company}\"")
                return {"Error":-1}

    #Sends data to a device
    def sendData(self, datapoint:str, value:any):
        #Checks what company the device is from
        match(self.company):
            #If it is a Tuya Device
            case "Tuya":
                apiDevice = tuya.Device(dev_id=self.id, address=self.ip, local_key=self.key, version=self.version)
                #Gets the mapping
                for mapping in self.mappings.keys():
                    if(self.mappings[mapping] == datapoint or mapping == datapoint):
                        apiDevice.set_value(mapping, value, nowait=True)
            #Invalid Companies
            case _:
                addToErrorLog(f"Invalid Company '{self.company}'")
            
##FUNCTION DEFINITIONS##
#Loads a Device From the Database
def loadDeviceFromDatabase(id:str) -> Device:
    cursor = app.config['cursor']
    query = ("SELECT * FROM devices "
                "WHERE DeviceID = %s")

    cursor.execute(query, (id,))
    device = cursor.fetchone()
    if(device == None):
        return None

    return Device(id=device['DeviceID'], name=device['DeviceName'], ip=device['IpAddress'], key=device['Key'], version=device['Version'], company=device['Company'])