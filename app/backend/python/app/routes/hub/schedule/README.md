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
-	(small int)IsPublic - Holds value 0 or 1 representing if schedule is public to all users (Does Nothing Yet)
-	(int)Rating – Rating given by other users, NULL if IsPublic is 0 and was never 1
-	(dict[])Code – List of function blocks that make up the code for specified schedule
-	(dict)Trigger – Dictionary of DeviceIDs as keys paired with string of array holding data
<br><br><br><br>

## Routes

### ‘/hub/[HubID]/schedule’

#### Methods: 
-	GET
-	POST
-   DELETE

#### Prerequisites: 
-	User Logged In
    -	Session ID Cookie set
<br>

#### GET: 

Lists ID, Name, Active status, Full name of author and auther's permission levels for all schedules in hub.
Current User must be part of hub and have permission level > 1.

##### Required Parameters:

##### Return Values:
-	(string)ScheduleID – Unique ID to identify specified schedule
-	(string)ScheduleName – Name of schedule
-   (small int)IsActive - boolean to represent if schedule is set active (1 if active, 0 if not)
-   (string)Author - Full name of author of schedule
-   (int)PermissionLevel - Permission level granted to author of schedule
<br>

<br><br><br>

### '/hub/[HubID]/schedule/[ScheduleID]'

#### Methods:
-   GET
-   PATCH
-   DELETE

#### Prerequisites: 
-	User Logged In
    -	Session ID Cookie set
<br>

#### GET: 

Lists full details of specified schedule in hub.
See [schedule doc](.../schedule/README.md) if required.
Current User must be part of hub with view access.

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

TO DO:
GET schedules - done
add schedules
delete schedules
update schedules
create schedules

<br><br><br><br>

### LINK TO RELATED DOCS
#### [Schedule Doc](.../schedule/README.md)
#### [Hub Doc](../README.md)
#### [Hub User Doc](../user/README.md)