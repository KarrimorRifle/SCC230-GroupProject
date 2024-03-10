# Hub Routes
###### Refer back to iota classes as well for more information.
<br><br>
### LINK TO RELATED DOCS
#### [Hub User Doc](./user/README.md)
<br><br>
## Classes
###### *for frontend to worry about by backend
<br>

### Hub

Hub model as handled by backend for database storing. The data in DB is processed slightly differently when handed to iota manager to create and use as a schedule class object. 

Structure shows variables and values for frontend to be familiar with.

#### Structure:
-	(string)HubID – Unique ID to identify specified Hub
-	(string)HubName – Name of Hub
<br>

### Hub_User

Hub member model as handled by backend for database storing. The data in DB is processed slightly differently when handed to iota manager to create and use as a schedule class object. 

Structure shows variables and values for frontend to be familiar with.

#### Structure:
-	(string)HubID – Unique ID to identify specified Hub
-	(string)AccountID – Unique ID to identify specified Account
-   (int)PermissionLevel - integer suggesting perms of user (0-5)
    -   increasing perm levels have rights of all previous levels
    -   0: No rights
    -   1: View rights
    -   2: Activation/Deactivation rights
    -   3: Edit/Create/Delete rights
    -   4: Admin rights (adding/removing/managing users of lower perm)
    -   5: Owner rights (Can edit/delete hub)

 <br><br><br><br>
## Routes

### ‘/hub’

#### Methods: 
-	GET
-	POST

#### Prerequisites: 
-	User Logged In
    -	Session ID Cookie set
<br>

#### GET: 

Lists ID, Name of all hubs current user is in.

##### Required Parameters:

##### Return Values:
-	(string)HubID – Unique ID to identify specified hub
-	(string)HubName – Name of hub
-   (int)PermissionLevel - Permission level of the current user
<br>

#### POST:

Creates new hub under ID of current user.

##### Required Parameters:
-   (string)HubName - Name of hub

##### Return Values:
-	(string)HubID – Unique ID to identify specified hub
-	(string)HubName – Name of hub
<br><br><br>

### ‘/hub/[HubID]’

#### Methods: 
-	GET
-	DELETE
-   PATCH

#### Prerequisites: 
-	User Logged In
    -	Session ID Cookie set
<br>

#### GET: 

Lists ID, Name of specified hub current user is in.

##### Required Parameters:

##### Return Values:
-	(string)HubID – Unique ID to identify specified hub
-	(string)HubName – Name of hub
-   (int)PermissionLevel - Permission level of the current user
<br>

#### DELETE:

Delete hub under ID of current user if has perms.

##### Required Parameters:

##### Return Values:
-	(string)HubID – Unique ID to identify specified hub
<br>

#### PATCH: 

Updates specified hub data based on passed parameters if user has perms.

##### Optional Parameters:
-	(string)HubName – Name of hub

##### Return Values:
-	(string)HubID – Unique ID to identify specified hub
-	(string)HubName – Name of hub
-   (int)PermissionLevel - Permission level of the current user

<br><br><br><br>


### LINKS TO RELATED DOCS <br>
#### [Hub User Doc](./user/README.md)
