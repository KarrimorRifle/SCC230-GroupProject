# [Backend/Python/App/Iota/Device.py](../python/app/iota/Device.py)
# Classes
## Device
### Description
Class to hold information about IOT Devices

### Values
- (str) id - Holds the ID for the Device to be stored in the Database
- (str) name - Holds the name that the user will see for the Device
- (bool) isActive - Whether or not a Device is currently in use
- ({str:any}) data - The Data that is currently stored in the device 
- (bool) debug - Whether the class should print statements for debugging

### Constructor
**Required Parameters**
- self
- (str) id - The value the object's id variable is set to
- (str) name - The value the object's name variable is set to
**Optional Parameters**
- (bool) isActive - The value the object's isActive variable is set to
- (bool) debug - The value the object's debug variable is set to

### Public Methods
- updateData(self)\
  **Description**\
  Updates the data stored within the device
  
  **Return Value**\
  ({str: any}) The updated data of the device
  
- checkConnection(self)\
  **Description**\
  Checks whether or not the device can be connected to

  **Return Value**\
  (bool) whether or not the device was connected to

# Functions
- loadDeviceFromDatabase(id)\
  **Description**
  Loads a Device from the database, based on it's ID
  **Required Parameters**
  - (str) id - The ID of the Device that is being retrieved.
  
  **Return Value**\
  (Device) The Device stored in the database
