# [Backend/Python/App/Iota/Trigger.py](../python/app/iota/Trigger.py)
# Required Modules
## iota
[Documentation](Iota-__init__-Documentation.md)\
[File](../python/app/iota/__init__.py)

## iota.Device
[Documentation](Iota-Device-Documentation.md)\
[File](../python/app/iota/Device.py)

## iota.Schedule
[Documentation](Iota-Schedule-Documentation.md)\
[File](../python/app/iota/Schedule.py)

## server
[Documentation]()\
[File](../python/app/server.py)

## threading
[Documentation](https://docs.python.org/3/library/threading.html)

# Classes
## Trigger
### Description
---
Class to Hold information about a "Trigger", a condition that needs to become true in order for a schedule to run

### Values
---
- (str) id - The unique ID for the Trigger.
- ([Device]) devices - The Devices that the Trigger references.
- ([str]) data - The condition that the Trigger Needs to meet in order to activate.
- (str) ScheduleID - The ID of the schedule that the Trigger will activate.
- (bool) canRun - Whether or not the trigger can activate it's linked schedule.
- (bool) debug - Whether the class should print statements for debugging.

### Constructor
---
**Required Parameters**
- (str) id - the value the object’s id variable is set to.
- (str) ScheduleID - the value the object’s Schedule variable is set to.
- ([str]) data - the value the object’s data variable is set to.

**Optional Parameters**
- (bool) canRun - the value the object’s canRun variable is set to.\
  Default Value: False
- (bool) debug - the value the object’s debug variable is set to.\
  Default Value: False
---

### Public Methods
---
- ***updateCanRun(self)***\
  **Description**\
  Updates the value of a Trigger's canRun variable in the database
---
### Private Methods
- ***\_\_resolveDatapoint(self, datapoint)***\
  **Description**
  Translates the value of a datapoint within the Trigger's data variable to an evaluable format\
  **Required Parameters**
  - (str) datapoint - The datapoint that is being resolved.
---
# Functions
- ***loadTriggerFromDatabase***\
  **Description**\
  Loads a Trigger from the database, based on it's ID
  
  **Required Parameters**
  - (str) id - The ID of the Trigger that is being retrieved.
  
  **Return Value**\
  (Trigger) The Trigger retrieved from the database
---
- ***getTriggerIDs()***\
  **Description**\
  Loads the list of all IDs from the database

  **Return Value**\
  ([str]) The IDs of all the Triggers in the Database
---
- ***checkTriggers(ids)***\
  **Description**\
  Individually checks whether or not each Trigger should be running, based on the data that it requests. 
  
  **Required Parameters**
  - ([str]) ids - the list of Trigger IDs that the function will request from the Database
---
- ***main()***\
 **Description**\
 Continuously runs checkTriggers, to see if any schedules need to be run
---