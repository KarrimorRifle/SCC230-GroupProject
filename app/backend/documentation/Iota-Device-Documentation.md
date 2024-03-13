# [Backend/Python/App/Iota/Device.py](../python/app/iota/Device.py)
# Required Modules
## iota
[Documentation](Iota-__init__-Documentation.md)\
[File](../python/app/iota/__init__.py)

## server
[Documentation]()\
[File](../python/app/server.py)

## tinytuya
[Documentation](https://pypi.org/project/tinytuya/1.1.2/)

# Constants
## TUYASERVER
- The cloud server with the user's available Tuya Devices on it.
- value: tuya.Cloud(Region, APIKey, APISecret)

# Classes
## Device
### Description
---
Class to control and hold information about IOT Devices

### Values
---
- (str) id - Holds the ID for the Device to be stored in the Database
- (str) name - Holds the name that the user will see for the Device
- (str) ip - Holds the IP of the device so that the program can send the device data
- (str) key - Holds the local key of the Device, needed to confirm it's being accessed consentually
- (float) version - Holds the API version that TinyTuya uses to communicate with the device
- ({int:str}) mappings - Maps the Datapoint's number to it's code, so that the value can be accessed by name.
- ({str:str}) typeMappings - Maps the Datapoint's code to it's Type, so that the values the user can send are restricted
- ({str:any}) data - The Data that is currently stored in the device 
- (bool) debug - Whether the class should print statements for debugging

### Constructor
---
**Required Parameters**
- (str) id - The value the object's id variable is set to
- (str) name - The value the object's name variable is set to
- (str) ip - The value the object's ip variable is set to

**Optional Parameters**
- (str) key - The value the object's key variable is set to\
  Default Value: ""
- (float) version - The value the object's version variable is set to\
  Default Value: 0.0
- (str) company - The value the object's company variable is set to\
  Default Value: "Tuya"
- (bool) debug - The value the object's debug variable is set to\
  Default Value: False

### Public Methods
---
- ***updateMappings(self)***\
  **Description**\
  retrieves the information needed to create the self.mappings and self.typeMappings variables.
---
- ***changeData(self, data)***\
  **Description**\
  Sends all the differences in data between what is currently in the device and the data list passed in.\
  **Required Parameters**
  - ({str:any}) data - The dictionary of datapoints:value that the device will receive as changes.
---
- ***updateData(self)***\
  **Description**\
  Updates the self.data dict to match the information stored within a device.
---
- ***sendData(self, datapoint, value)***\
  **Description**\
  Updates the device's value of a specific datapoint to be the passed value.\
  **Required Parameters**
  - (str) datapoint - The datapoint that is being updated.
  - (any) value - The value that the datapoint is being set to.
---
# Functions
- ***loadDeviceFromDatabase(id)***\
  **Description**
  Loads a Device from the database, based on it's ID
  **Required Parameters**
  - (str) id - The ID of the Device that is being retrieved.
  
  **Return Value**\
  (Device) The Device stored in the database
---