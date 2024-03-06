# Hub User Routes
###### Refer back to iota classes as well for more information.
<br><br>

### LINK TO RELATED DOCS
#### [Schedule Doc](.../schedule/README.md)
#### [Hub Doc](../README.md)
#### [Hub User Doc](../user/README.md)
<br><br>

## Classes
###### *for frontend to worry about by backend
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
-	(small int)IsPublic - Holds value 0 or 1 representing if schedule is public to all users
-   (string)CopyFrom - Holds ID of original creator of schedule template, NULL if current Author is original creator.
-	(int)Rating – Rating given by other users, NULL if IsPublic is 0 and was never 1
-	(dict[])Code – List of function blocks that make up the code for specified schedule
-	(dict)Trigger – Dictionary of DeviceIDs as keys paired with string of array holding data
<br><br><br><br>

## Routes

### ‘/hub/[HubID]/schedule’

#### Methods: 
-	GET
-	POST

#### Prerequisites: 
-	User Logged In
    -	Session ID Cookie set
<br>

#### GET: 

Lists ID, Name, Active status, Full name of author and auther's permission levels for all schedules in hub.
Current User must be part of hub and have permission level > 0.

##### Required Parameters:

##### Return Values:
-	(string)ScheduleID – Unique ID to identify specified schedule
-	(string)ScheduleName – Name of schedule
-   (small int)IsActive - boolean to represent if schedule is set active (1 if active, 0 if not)
-   (string)Author - Full name of author of schedule
-   (string)CopyFrom - Holds ID of original creator of schedule template, NULL if current Author is original creator.
-   (int)PermissionLevel - Permission level granted to author of schedule
<br>

#### POST: 

Create new empty schedule template and assign it to specified hub.
Current User must be part of hub and have permission level > 2.

##### Required Parameters:
-   (string)ScheduleName - Name of Schedule
##### Return Values:
-	(string)ScheduleID – Unique ID to identify specified schedule
-	(string)AuthorID - Unique ID to identify user who created specified schedule
-	(string)ScheduleName – Name of schedule
-   (string)HubID - Unique ID of hub schedule is in
-	(small int)IsActive – Holds value 0 or 1 representing active status of schedule
-	(small int)IsPublic - Holds value 0 or 1 representing if schedule is public to all users
-   (string)CopyFrom - Holds ID of original creator of schedule template, NULL if current Author is original creator.
-	(int)Rating – Rating given by other users, NULL if IsPublic is 0 and was never 1
-	(dict[])Code – List of function blocks that make up the code for specified schedule - will be empty
-	(dict)Trigger – Dictionary of DeviceIDs as keys paired with string of array holding data - will be empty

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

<br><br><br>

### '/hub/[HubID]/schedule/[ScheduleID]'

#### Methods:
-   GET
-   POST
-   DELETE
-   PATCH

#### Prerequisites: 
-	User Logged In
    -	Session ID Cookie set
<br>

#### GET: 

Lists full details of specified schedule in hub.
See [schedule doc](.../schedule/README.md) if required.
Current User must be part of hub with view access.
PermissionLevel > 0.

##### Required Parameters:

##### Return Values:
-	(string)ScheduleID – Unique ID to identify specified schedule
-	(string)AuthorID - Unique ID to identify user who created specified schedule
-	(string)ScheduleName – Name of schedule
-   (string)HubID - Unique ID of hub schedule is in
-	(small int)IsActive – Holds value 0 or 1 representing active status of schedule
-	(small int)IsPublic - Holds value 0 or 1 representing if schedule is public to all users
-   (string)CopyFrom - Holds ID of original creator of schedule template, NULL if current Author is original creator.
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

#### POST: 

Add to hub and Lists full details of specified schedule.
See [schedule doc](.../schedule/README.md) if required.
Current User must be part of hub with edit access.
PermissionLevel > 2.

##### Required Parameters:

##### Return Values:
-	(string)ScheduleID – Unique ID to identify specified schedule
-	(string)AuthorID - Unique ID to identify user who created specified schedule
-	(string)ScheduleName – Name of schedule
-   (string)HubID - Unique ID of hub schedule is in
-	(small int)IsActive – Holds value 0 or 1 representing active status of schedule
-	(small int)IsPublic - Holds value 0 or 1 representing if schedule is public to all users
-   (string)CopyFrom - Holds ID of original creator of schedule template, NULL if current Author is original creator.
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

Remove specified schedule in hub.
See [schedule doc](.../schedule/README.md) if required.
Current User must be part of hub with edit access.
PermissionLevel > 2.

##### Required Parameters:

##### Return Values:
-	(string)ScheduleID – Unique ID to identify specified schedule
<br>

#### PATCH: 

Update and Lists full details of specified schedule in hub.
See [schedule doc](.../schedule/README.md) if required.
Current User must be part of hub with edit access.
PermissionLevel > 2.

Same route works for toggle active and draft status of schedule in hub.
When used for this only IsActive and IsDraft params should be passed.
Current user must be part of hub with toggle activation access.
PermissionLevel > 1.

##### Optional Parameters:
-	(string)ScheduleName – Name of schedule
-	(small int)IsActive – Holds value 0 or 1 representing active status of schedule
    -   MUST BE THE ONLY Param PASSED EXCEPT IsDraft IF USER HAS ONLY TOGGLE ACTIVE ACCESS
-	(small int)IsDraft – Holds value 0 or 1 representing draft status of schedule
    -   MUST BE THE ONLY Param PASSED EXCEPT IsActive IF USER HAS ONLY TOGGLE ACTIVE ACCESS
-	(small int)IsPublic - Holds value 0 or 1 representing if schedule is public to all users
-	(dict[])Code – list of function blocks that make up the code for specified schedule
-	(dict)Trigger – dictionary of DeviceIDs as keys paired with string of array holding data

##### Return Values:
-	(string)ScheduleID – Unique ID to identify specified schedule
-	(string)AuthorID - Unique ID to identify user who created specified schedule
-	(string)ScheduleName – Name of schedule
-   (string)HubID - Unique ID of hub schedule is in
-	(small int)IsActive – Holds value 0 or 1 representing active status of schedule
-	(small int)IsPublic - Holds value 0 or 1 representing if schedule is public to all users
-   (string)CopyFrom - Holds ID of original creator of schedule template, NULL if current Author is original creator.
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

<br><br><br><br>

### LINK TO RELATED DOCS
#### [Schedule Doc](.../schedule/README.md)
#### [Hub Doc](../README.md)
#### [Hub User Doc](../user/README.md)