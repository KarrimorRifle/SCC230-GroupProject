# Hub User Routes
###### Refer back to iota classes as well for more information.
<br><br>

### LINK TO RELATED DOCS
#### [Hub Doc](../README.md)
<br><br>

## Classes
###### *for frontend to worry about by backend
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

### ‘/hub/[HubID]/user’

#### Methods: 
-	GET
-	POST
-   DELETE

#### Prerequisites: 
-	User Logged In
    -	Session ID Cookie set
<br>

#### GET: 

Lists ID, Full Name and Permission Level of all users in hub.
Current User must be part of hub.

##### Required Parameters:

##### Return Values:
-	(string)AccountID – Unique ID to identify specified user
-	(string)Name – Full Name of user
-   (int)PermissionLevel - Permission level granted to user
<br>

#### POST:

Force add a user to a hub, ONLY USE FOR TESTING PURPOSES.

##### Required Parameters:
-   (string)AccountID - Unique ID to identify specified user

##### Return Values:
-	(string)AccountID – Unique ID to identify specified user
-   (int)PermissionLevel - Permission level granted to user
<br>

#### DELETE:

Leave hub.

##### Required Parameters:

##### Return Values:
-	(string)HubID – Unique ID to identify specified hub
<br><br><br>

### '/hub/[HubID]/user/[AccountID]'

#### Methods:
-   GET
-   PATCH
-   DELETE

#### Prerequisites: 
-	User Logged In
    -	Session ID Cookie set
<br>

#### GET: 

Lists ID, Full Name and Permission Level of one user in hub.
Current User must be part of hub.

##### Required Parameters:

##### Return Values:
-	(string)AccountID – Unique ID to identify specified user
-	(string)Name – Full Name of user
-   (int)PermissionLevel - Permission level granted to user
<br>

#### PATCH: 

Update Permission Level of one user in hub.
Current User must be part of hub.
Current User must be permission level 4 or higher.
Current User must have higher permission level.

##### Required Parameters:
-   (int)PermissionLevel - Permission level to be set (must be lower than that of current user)

##### Return Values:
-	(string)AccountID – Unique ID to identify specified user
-	(string)Name – Full Name of user
-   (int)PermissionLevel - Permission level granted to user
<br>

#### DELETE: 

Delete Permission Level of one user in hub.
Current User must be part of hub.
Current User must be permission level 4 or higher.
Current User must have higher permission level.

##### Required Parameters:

##### Return Values:
-	(string)AccountID – Unique ID to identify specified user
-	(string)HubID - Unique ID to identify specified hub
<br><br><br>

### '/hub/[HubID]/invite'

#### Methods:
-   POST

#### Prerequisites: 
-	User Logged In
    -	Session ID Cookie set
<br>

#### POST: 

Creates invite token for hub.
Current user must be permission level 4 or higher

##### Required Parameters:

##### Return Values:
-	(string)HubID – Unique ID to identify specified hub
-	(string)Token - invite token to allow other users to join hub
    -   This token expires in 1 day
<br><br><br>

### '/hub/invite/[Token]'

#### Methods:
-   POST

#### Prerequisites: 
-	User Logged In
    -	Session ID Cookie set
<br>

#### POST: 

Join hub via token.
Token must still be valid.
Joining users will by default be permission level 1.

##### Required Parameters:

##### Return Values:
-	(string)HubID – Unique ID to identify specified hub
<br><br><br><br>


### LINKS TO RELATED DOCS <br>
#### [Hub Doc](../README.md)
