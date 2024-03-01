# Hub User Routes
###### Refer back to iota classes as well for more information.

#### [Hub Doc](../README.md)

## Routes

### ‘/hub/[HubID]/user’

#### Methods: 
-	GET
-	POST
-   DELETE

#### Prerequisites: 
-	User Logged In
    -	Session ID Cookie set

#### GET: 

Lists ID, Full Name and Permission Level of all users in hub.
Current User must be part of hub.

##### Required Parameters:

##### Return Values:
-	(string)AccountID – Unique ID to identify specified user
-	(string)Name – Full Name of user
-   (int)PermissionLevel - Permission level granted to user

#### POST:

Force add a user to a hub, ONLY USE FOR TESTING PURPOSES.

##### Required Parameters:
-   (string)AccountID - Unique ID to identify specified user

##### Return Values:
-	(string)AccountID – Unique ID to identify specified user
-   (int)PermissionLevel - Permission level granted to user

#### DELETE:

Leave hub.

##### Required Parameters:

##### Return Values:
-	(string)HubID – Unique ID to identify specified hub

### '/hub/[HubID]/user/[AccountID]'

#### Methods:
-   GET
-   PATCH
-   DELETE

#### Prerequisites: 
-	User Logged In
    -	Session ID Cookie set

#### GET: 

Lists ID, Full Name and Permission Level of one user in hub.
Current User must be part of hub.

##### Required Parameters:

##### Return Values:
-	(string)AccountID – Unique ID to identify specified user
-	(string)Name – Full Name of user
-   (int)PermissionLevel - Permission level granted to user

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

#### DELETE: 

Delete Permission Level of one user in hub.
Current User must be part of hub.
Current User must be permission level 4 or higher.
Current User must have higher permission level.

##### Required Parameters:

##### Return Values:
-	(string)AccountID – Unique ID to identify specified user
-	(string)HubID - Unique ID to identify specified hub

### '/hub/[HubID]/invite'

#### Methods:
-   POST

#### Prerequisites: 
-	User Logged In
    -	Session ID Cookie set

#### POST: 

Creates invite token for hub.
Current user must be permission level 4 or higher

##### Required Parameters:

##### Return Values:
-	(string)HubID – Unique ID to identify specified hub
-	(string)Token - invite token to allow other users to join hub
    -   This token expires in 1 day

### '/hub/invite/[Token]'

#### Methods:
-   POST

#### Prerequisites: 
-	User Logged In
    -	Session ID Cookie set

#### POST: 

Join hub via token.
Token must still be valid.
Joining users will by default be permission level 1.

##### Required Parameters:

##### Return Values:
-	(string)HubID – Unique ID to identify specified hub