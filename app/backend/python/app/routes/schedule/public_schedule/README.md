# Public Schedule Routes
###### Refer back to iota classes as well for more information.
<br><br>

### LINK TO RELATED DOCS
#### [Schedule Doc](../README.md)
#### [Hub Schedule Doc](../../hub/schedule/README.md)
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
-   (string)Description - Description of Schedule
-   (string)HubID - Unique ID of hub schedule is in
-	(small int)IsActive – Holds value 0 or 1 representing active status of schedule
-	(small int)IsDraft – Holds value 0 or 1 representing draft status of schedule
-   (string)CopyFrom - Holds ID of original creator of schedule template, NULL if current Author is original creator.
-	(small int)IsPublic - Holds value 0 or 1 representing if schedule is public to all users
-	(int)Rating – Rating given by other users, NULL if IsPublic is 0 and was never 1
-	(dict[])Code – List of function blocks that make up the code for specified schedule
-	(string[])Trigger – array holding data for trigger
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

### ‘/schedule/public’

#### Methods: 
-	GET

#### Prerequisites: 
-	User Logged In
    -	Session ID Cookie set
<br>

#### GET: 

Lists ScheduleID, ScheduleName, Rating active and draft status of all public schedules.

##### Required Parameters:

##### Return Values:
-	(string)ScheduleID – Unique ID to identify specified schedule
-	(string)ScheduleName – Name of schedule
-	(small int)IsActive – Holds value 0 or 1 representing active status of schedule
-	(small int)IsDraft – Holds value 0 or 1 representing draft status of schedule
-	(small int)IsPublic - Holds value 0 or 1 representing if schedule is public to all users
-   (string)CopyFrom - Holds ID of original creator of schedule template, NULL if current Author is original creator.
-	(int)Rating – Rating given by other users, should be NULL if IsPublic is 0 and was never 1

<br><br><br>

### ‘/schedule/public/[ScheduleID]’

#### Methods: 
-	GET
-   POST
-   PATCH

#### Prerequisites: 
-	User Logged In
    -	Session ID Cookie set
<br>

#### GET: 

Lists all values associated with public schedule specified by ID in url.

##### Required Parameters:

##### Return Values:
-	(string)ScheduleID – Unique ID to identify specified schedule
-	(string)AuthorID - Unique ID to identify user who created specified schedule
-	(string)ScheduleName – Name of schedule
-   (string)Description - Description of Schedule
-   (string)HubID - Unique ID of hub schedule is in
-	(small int)IsActive – Holds value 0 or 1 representing active status of schedule
-	(small int)IsDraft – Holds value 0 or 1 representing draft status of schedule
-	(small int)IsPublic - Holds value 0 or 1 representing if schedule is public to all users
-   (string)CopyFrom - Holds ID of original creator of schedule template, NULL if current Author is original creator.
-	(int)Rating – Rating given by other users, NULL if IsPublic is 0 and was never 1
-	(dict[])Code – List of function blocks that make up the code for specified schedule
-	(string[])Trigger – array holding data for trigger

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

<br>

#### POST: 

Create duplicate of public schedule with current user as author and original author listed under CopyFrom field.

##### Required Parameters:

##### Return Values:
-	(string)ScheduleID – Unique ID to identify specified schedule
-	(string)AuthorID - Unique ID to identify user who created specified schedule
-	(string)ScheduleName – Name of schedule
-   (string)Description - Description of Schedule
-   (string)HubID - Unique ID of hub schedule is in
-	(small int)IsActive – Holds value 0 or 1 representing active status of schedule
-	(small int)IsDraft – Holds value 0 or 1 representing draft status of schedule
-	(small int)IsPublic - Holds value 0 or 1 representing if schedule is public to all users
-   (string)CopyFrom - Holds ID of original creator of schedule template, NULL if current Author is original creator.
-	(int)Rating – Rating given by other users, NULL if IsPublic is 0 and was never 1
-	(dict[])Code – List of function blocks that make up the code for specified schedule
-	(string[])Trigger – array holding data for trigger

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

<br>

#### PATCH: 

Updates rating of public schedule based on current user's rating.

##### Required Parameters:
-   (int)Rating - User rating for a schedule from 0 to 5

##### Return Values:
-	(string)ScheduleID – Unique ID to identify specified schedule
-	(int)Rating – Rating given by other users, NULL if IsPublic is 0 and was never 1

<br><br><br>

### ‘hub/[HubID]/schedule/public/[ScheduleID]’

#### Methods: 
-   POST

#### Prerequisites: 
-	User Logged In
    -	Session ID Cookie set
<br>

#### POST: 

Create duplicate of public schedule and add it to specified hub with current user as author and original author listed under CopyFrom field.

##### Required Parameters:

##### Return Values:
-	(string)ScheduleID – Unique ID to identify specified schedule
-	(string)AuthorID - Unique ID to identify user who created specified schedule
-	(string)ScheduleName – Name of schedule
-   (string)Description - Description of Schedule
-   (string)HubID - Unique ID of hub schedule is in
-	(small int)IsActive – Holds value 0 or 1 representing active status of schedule
-	(small int)IsDraft – Holds value 0 or 1 representing draft status of schedule
-	(small int)IsPublic - Holds value 0 or 1 representing if schedule is public to all users
-   (string)CopyFrom - Holds ID of original creator of schedule template, NULL if current Author is original creator.
-	(int)Rating – Rating given by other users, NULL if IsPublic is 0 and was never 1
-	(dict[])Code – List of function blocks that make up the code for specified schedule
-	(string[])Trigger – array holding data for trigger

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

<br><br><br><br>

### LINK TO RELATED DOCS
#### [Schedule Doc](../README.md)
#### [Hub Schedule Doc](../../hub/schedule/README.md)