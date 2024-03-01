# Schedule Routes
###### Refer back to iota classes as well for more information.
<br><br>

### LINK TO RELATED DOCS
#### [Schedule Doc](../hub/schedule/README.md)
<br><br>

## Classes
###### *for frontend to worry about by backend
<br>

### Trigger

Dictionary using valid DeviceIDs as keys and string arrays as values.

No need for frontend to deal with TriggerIDs as triggers are directly connected to the schedules they are made for when updating said schedules.

#### Structure:
-	(dict)Trigger – {DeviceID: data}
    -	DeviceID(Key) – Valid ID of a connected device
    -	Data(Value) – Array of string values (Refer to iota class docs for details on format and structure)
<br>

### Schedule

Schedule model as handled by backend for database storing. The data in DB is processed slightly differently when handed to iota manager to create and use as a schedule class object. 

Structure shows variables and values for frontend to be familiar with.

#### Structure:
-	(string)ScheduleID – Unique ID to identify specified schedule
-	(string)AuthorID - Unique ID to identify user who created specified schedule
-	(string)ScheduleName – Name of schedule
-   (string)HubID - Unique ID of hub schedule is in
-	(small int)IsActive – Holds value 0 or 1 representing active status of schedule
-	(small int)IsPublic - Holds value 0 or 1 representing if schedule is public to all users (Does Nothing Yet)
-	(int)Rating – Rating given by other users, NULL if IsPublic is 0 and was never 1
-	(dict[])Code – List of function blocks that make up the code for specified schedule
-	(dict)Trigger – Dictionary of DeviceIDs as keys paired with string of array holding data
<br>

### Function Block

Singular code block, array of function blocks together make up Code. 

Individual function blocks within a schedule are treated as dictionaries.

#### Structure:
-	(dict)Block - {'CommandType': string, 'Number': int, 'LinkedCommands': list[int], 'Params': list[string]}
-	(string)CommandType - String referencing type of function block
-	(int)Number - Position of function block in code
-	(int[])LinkedCommands - List of positions of blocks linked to current block
-	(string[])Params - List of values used as parameters in the function block
 <br><br><br><br>
 
## Routes

### ‘/schedule’

#### Methods: 
-	GET
-	POST

#### Prerequisites: 
-	User Logged In
    -	Session ID Cookie set
<br>

#### GET: 

Lists ID, Name and Status of all schedules created by current user.

##### Required Parameters:

##### Return Values:
-	(string)ScheduleID – Unique ID to identify specified schedule
-	(string)ScheduleName – Name of schedule
-	(small int)IsActive – Holds value 0 or 1 representing active status of schedule
-	(small int)IsPublic - Holds value 0 or 1 representing if schedule is public to all users (Does Nothing Yet)
-	(int)Rating – Rating given by other users, should be NULL if IsPublic is 0 and was never 1

<br>

#### POST: 

Creates a new empty schedule under ID of current user.

##### Required Parameters:
-	(string)ScheduleName – Name of schedule
-	(small int)IsActive – Holds value 0 or 1 representing active status of schedule
-	(small int)IsPublic - Holds value 0 or 1 representing if schedule is public to all users (Does Nothing Yet)
-	(int)Rating – Rating given by other users, NULL if IsPublic is 0

##### Return Values:
-	(string)ScheduleID – Unique ID to identify new schedule

 <br><br><br>
 
### ‘/schedule/[ScheduleID]’

#### Methods: 
-	GET
-	DELETE
-	PATCH

#### Prerequisites: 
-	User Logged In
    -	Session ID Cookie set
-	[ScheduleID] is a valid ID of a schedule belonging to current user
<br>

#### GET: 

Lists all values associated with schedule belonging to current user specified by ID in url.

##### Required Parameters:

##### Return Values:
-	(string)ScheduleID – Unique ID to identify specified schedule
-	(string)AuthorID - Unique ID to identify user who created specified schedule
-	(string)ScheduleName – Name of schedule
-   (string)HubID - Unique ID of hub schedule is in
-	(small int)IsActive – Holds value 0 or 1 representing active status of schedule
-	(small int)IsPublic - Holds value 0 or 1 representing if schedule is public to all users (Does Nothing Yet)
-	(int)Rating – Rating given by other users, NULL if IsPublic is 0 and was never 1
-	(dict[])Code – List of function blocks that make up the code for specified schedule
-	(dict)Trigger – Dictionary of DeviceIDs as keys paired with string of array holding data

##### Structure of Code:
-	List of function block dictionaries
-	Function block structure:
    -	{'CommandType': string, 'Number': int, 'LinkedCommands': list[int], 'Params': list[string]}
    -	CommandType – String referencing type of function block
        -	Valid Types: ‘FOR’, ‘WHILE’, ‘IF’, ‘ ELSE’, ‘SET’, ‘END’
    -	Number – Position of function block in code
    -   LinkedCommands – List of positions of blocks linked to current block
    -	Params – List of values used as parameters in the function block
        -	Refer to iota class docs by Kian for details regarding structure

##### Structure of Trigger:
-	Dictionary with DeviceIDs and data
-	Trigger dictionary structure:
    -	{DeviceID: string[], DeviceID: string[], DeviceID: string[], … }
<br>

#### DELETE: 

Deletes schedule specified by ID given in url.

##### Required Parameters:

##### Return Values:
-	(string)ScheduleID – Unique ID of deleted schedule
 
<br>

#### PATCH: 

Updates specified schedule data based on passed parameters.

##### Optional Parameters:
-	(string)ScheduleName – Name of schedule
-	(small int)IsActive – Holds value 0 or 1 representing active status of schedule
-	(small int)IsPublic - Holds value 0 or 1 representing if schedule is public to all users (Does Nothing Yet)
-	(int)Rating – Rating given by other users, NULL if IsPublic is 0 and was never 1
-	(dict[])Code – list of function blocks that make up the code for specified schedule
-	(dict)Trigger – dictionary of DeviceIDs as keys paired with string of array holding data

##### Structure of Code:
-	List of function block dictionaries
-	Function block structure:
    -	{'CommandType': string, 'Number': int, 'LinkedCommands': list[int], 'Params': list[string]}
    -	CommandType – String referencing type of function block
        -	Valid Types: ‘FOR’, ‘WHILE’, ‘IF’, ‘ ELSE’, ‘SET’, ‘END’
    -	Number – Position of function block in code
    -	LinkedCommands – List of positions of blocks linked to current block
    -	Params – List of values used as parameters in the function block
        -	Refer to iota class docs by Kian for details regarding structure

##### Structure of Trigger:
-	Dictionary with DeviceIDs and data
-	Trigger dictionary structure:
    -	{DeviceID: string[], DeviceID: string[], DeviceID: string[], … }

##### Return Values:
-	(string)ScheduleID – Unique ID to identify specified schedule
<br><br><br><br>

### LINK TO RELATED DOCS
#### [Hub Doc](../hub/schedule/README.md)