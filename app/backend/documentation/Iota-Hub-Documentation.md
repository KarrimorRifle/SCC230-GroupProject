# [Backend/Python/App/Iota/Hub.py](../python/app/iota/Hub.py)
# Required Modules
## iota.Schedule
[Documentation](Iota-Schedule-Documentation.md)\
[File](../python/app/iota/Schedule.py)

## iota.User
[Documentation](Iota-User-Documentation.md)\
[File](../python/app/iota/User.py)

## server
[Documentation]()\
[File](../python/app/server.py)

# Classes
## Hub
### Description
---
A class to act as the bridge between Schedules and their Users

### Values
---
- (str) id - Holds the ID for the hub to be stored in the database
- (str) name - Holds the name the user will see for the hub
- (str) address - Holds the address that is tied to the hub
- ([str]) logs - Holds the previous actions of the hub
- ({User:int}) users - Holds the users that are on the hub and their permission levels
- ([Schedule]) schedules - Holds the schedules that the hub is related to
- ([Device]) devices - Holds the Devices that are on the hub
- (bool) debug - Whether the hub class should output debug statements

### Constructor
---
**Required Parameters:**
- (str) id - the value the object’s id variable is set to.
- (str) name - the value the object’s name variable is set to.

**Optional Parameters:**
- (str) address - the value the object’s address variable is set to.\
  Default Value: ""
- ([str]) logs - the value the object’s logs variable is set to.\
  Default Value: []
- ({User:int}) users - the value the object’s users variable is set to.\
  Default Value: {}
- ([Schedules]) schedules - the value the object’s schedules variable is set to.\
  Default Value: []
- (bool) debug - the value the object’s isPublic debug is set to.\
  Default Value: False
---
# Functions
- ***loadHubFromDatabase(id)***\
  **Description**\
  Loads a Hub from the database, based on it's ID
  
  **Required Parameters**
  - (str) id - The ID of the Hub that is being retrieved.
  
  **Return Value**\
  (Hub) the Hub retrieved from the database
---