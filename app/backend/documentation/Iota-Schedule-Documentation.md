# [Backend/Python/App/Iota/Schedule.py](../python/app/iota/Schedule.py)
# Required Modules
## iota.Device
[Documentation](Iota-Device-Documentation.md)\
[File](../python/app/iota/Device.py)

## server
[Documentation]()\
[File](../python/app/server.py)

## threading
[Documentation](https://docs.python.org/3/library/threading.html)

## time
[Documentation](https://docs.python.org/3/library/time.html)

# Constants
## COMM_ELSE
- One of the valid commandTypes for the FunctionCode Class.
- COMM_ELSE FunctionCodes act as both ELSE statements and ELSE IF statements.
- COMM_ELSE FunctionCodes should have linkedCommands[] initialised with the IF statement that the ELSE statement is linked to, and any related COMM_ELSE commands that are acting as ELSE IF statements.
- COMM_ELSE statements can have either 0 or (3+4x) values stored in params[]. COMM_ELSE FunctionCodes with 0 params will be treated as an ELSE statement, COMM_ELSE FunctionCodes with 3+ will be treated as an ELSE IF statement, where params[] is the expression the ELSE IF statement will check. When params[] has values, it must be formatted as:\
  [value, operator, value, logical expression, value, operator, value, logical expression…]. For example:\
  ['x', '=', '1', 'or', 'y', '>=', '2']
- value: "ELSE"

## COMM_END
- One of the valid commandTypes for the FunctionCode.
- COMM_END FunctionCodes act as indicators for the end of a conditional statement, such as COMM_IF or COMM_WHILE FunctionCodes.
- COMM_END FunctionCodes should have linkedCommands[] initialised with the conditional FunctionCode that they are linked to.
- COMM_END FunctionCodes have nothing needed to be stored in params[].
- value: "END"

## COMM_FOR
- One of the valid commandTypes for the FunctionCode.
- COMM_FOR FunctionCodes act as FOR loops.
- COMM_FOR FunctionCodes have nothing needed to be stored in linkedCommands[].
- COMM_FOR FunctionCodes take 1 value in params[], the number of times that it should repeat the code attached to it. params[] must be formatted as:\
  [value]. For example:\
  ['60']
- value: "FOR"

## COMM_IF
- One of the valid commandTypes for the FunctionCode.
- COMM_IF FunctionCodes act as IF statements.
- COMM_IF FunctionCodes have nothing needed to be stored in linkedCommands[].
- COMM_IF statements should have (3+4x) values stored in params[], where params[] is the expression the IF statement will check.. params[] must be formatted as:\
  value, operator, value, logical expression, value, operator, value, logical expression…].For example:\
  ['x', '=', '1', 'or', 'y', '>=', '2']
- value: "IF"

## COMM_SET
- One of the valid commandTypes for the FunctionCode.
- COMM_SET FunctionCodes allow the user to set values stored throughout the schedule, or the values that devices have.
- COMM_SET FunctionCodes have nothing needed to be stored in linkedCommands[].
- COMM_SET FunctionCodes take 3 values in params[], the value that it needs to change, the operation that will be performed on it and the value it will be changed to/by. params[] must be formatted as:\
  [value, operation, value]. For example:\
  ['smartLight.brightness', '+=', '80']
- value: "SET"

## COMM_WAIT
- One of the valid commandTypes for the FunctionCode.
- COMM_WAIT FunctionCodes send the thread that they are on to sleep for params\[0] seconds.
- COMM_WAIT FunctionCodes have nothing needed to be stored in linkedCommands[].
- COMM_WAIT FunctionCodes take 1 value in params, the number of seconds the thread is sent to sleep for. params[] must be formatted as:\
  [seconds]. For example:\
  [60]
- value: "WAIT"

## COMM_WHILE
- One of the valid commandTypes for the FunctionCode.
- COMM_WHILE FunctionCodes act as WHILE loops.
- COMM_WHILE FunctionCodes have nothing needed to be stored in linkedCommands[].
- COMM_WHILE statements should have (3+4x) values stored in params[], where params[] is the expression the WHILE statement will continually check until it is false. params[] must be formatted as:\
  [value, operator, value, logical expression, value, operator, value, logical expression…]. For example:\
  ['x', '=', '1', 'or', 'y', '>=', '2']
- value = "WHILE"

# Classes
## FunctionCode
### Description
---
This class holds the information for a single operation for the iota CodeBlocks language, allowing the CodeBlocks to be interpreted to python.

### Values
---
- (str) commandType - The type of command the code is, for translating to python. Can be FOR, WHILE, IF, OTHERWISE, SET, GET or END.
- (int) number - Which FunctionCode of commandType the code is.
- (str) name - The unique name of the command, comprised of the commandType & number.
- ([FunctionCode]) linkedCommands - The FunctionCodes this FunctionCode is associated with.
- ([str]) params - The params that the command takes.
- (bool) hasRun - The number of times a FunctionCode has run

### Constructor
---
**Required Parameters:**
- self
- (str) commandType - The value the object’s commandType is set to.
- (int) number - The value the object’s number is set to.
  
**Optional Parameters:**
- ([FunctionCode]) linkedCommands - The value the object’s linkedCommands variable is set to.
  - Default value: []
- ([str]) params - The value the object’s params variable is set to.
  - Default value: []
  
## Schedule
### Description
Class to hold and run user-defined code when a trigger is activated.

### Values
- (str) id - The unique ID for the Schedule.
- (str) name - The name that the user sets for the Schedule.
- (bool) isPublic - Whether the Schedule can be seen by other users.
- (int) rating - The sum of positive and negative ratings given to the Schedule.
- ([FunctionCode]) code - The code that is run when a trigger is activated.
- ([Device]) Devices - The devices that the schedule needs to connect to in order to run.
- ({str: str}) Variables – Holds variables for the user to set and retrieve
- (bool) isRunnning - Whether the Schedule is currently running.
- (bool) isActive - Whether the User wants the Schedule to run when the trigger activates.
- (bool) debug - Whether the class should print statements for debugging

### Constructor
---
**Required Parameters:**
- (str) id - the value the object’s id is set to.
- (str) name - the value the object’s name is set to.
  
**Optional Parameters:**
- (bool) isPublic - the value the object’s isPublic variable is set to.\
  Default Value: False
- (int) rating - the value the object’s rating is set to\
  Default Value: 1
- ([Trigger]) triggers - the value the object’s triggers variable is set to\
  Default Value: []
- ([FunctionCode]) code - the value the object’s code variable is set to\
  Default Value: []
- (bool) isActive - the value the object’s isActive variable is set to\
  Default Value: False
- (bool) debug - the value the object's debug variable is set to\
  Default Value: False
---
### Public Methods
---
- ***runCode(self)***\
  **Description**\
  Runs the code stored in code, by calling the __translateSchedule function repeatedly and then resetting the values
---
- ***findDevices(self)***\
  **Description**\
  Gets the list of all devices by analysing the code value
  
  **Return Value**\
  ([Devices]) The list of devices the Schedule uses.
---
### Private Methods
---
- ***\_\_translateSchedule(self, index)***\
  **Description**\
  A recursive function called by runCode that interprets self.code to a python script that can then be run.
  
  **Optional Parameters**
  - (int) index - the index of the FunctionCode in self.code that is being translated.\
    Default Value: 0
    
  **Return Value**\
  (int) Returns the next position of index so that the code can be continually called until the end of the program
---
- ***\_\_runConditional(self, index)***\
  **Description**\
  A supporting function called by __translateSchedule that Translates all the FunctionCodes in a conditional statement or Loop.
  
  **Required Parameters**
  - (int) index - the index of the FunctionCode in self.code that the function starts its loop at.
---
- ***\_\_findEnd(self, index, statement)***\
  **Description**\
  A supporting function called by __translateSchedule that searches for where the end of a specific conditional or loop statement ends. Analogous to finding the matching } to a {.
  
  **Required Parameters**
  - (int) index - the index of the FunctionCode in self.code that the function starts looking for the end from.
  - (FunctionCode) statement - the statement that __FindEnd is looking for the end to.

  **Return Value**\
  (int) The index that the end of the conditional statement/loop is at.
---
- ***\_\_resetCounts(self)***\
  **Description**\
  A supporting function called by runCode that resets how many times a FunctionCode has run.
---
- ***\_\_resolveVariable(self, variable)***\
  **Description**\
  This function will check if the variable is custom (indicated by the prefix "var."), referenecs a device (indicated by the prefix "{DeviceID}.") or a constant value such as a string or float.
  
  **Required Parameters**
  - (str) variable - the variable that is being resolved
    
  **Return Value**\
  (str) The string in a format that allows it to be passed into a python
  eval/exec function

---
# Functions
- ***loadScheduleFromDatabase(id)***\
  **Description**\
  Loads a Schedule from the database, based on it's ID
  
  **Required Parameters**
  - (str) id - The ID of the Schedule that is being retrieved.
  
  **Return Value**\
  (Schedule) The Schedule retrieved from the database
---