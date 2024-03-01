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
-	(small int)IsActive – Holds value 0 or 1 representing active status of schedule
-	(small int)IsPublic - Holds value 0 or 1 representing if schedule is public to all users (Does Nothing Yet)
-	(int)Rating – Rating given by other users, NULL if IsPublic is 0 and was never 1
-	(dict[])Code – List of function blocks that make up the code for specified schedule
-	(dict)Trigger – Dictionary of DeviceIDs as keys paired with string of array holding data
<br><br><br><br>

<br><br><br><br>

### LINK TO RELATED DOCS
#### [Hub Doc](../README.md)
#### [Hub User Doc](../user/README.md)