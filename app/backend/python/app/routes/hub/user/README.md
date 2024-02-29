# Hub User Routes
###### Refer back to iota classes as well for more information.

#### [Hub Doc](../README.md)

## Routes

### ‘/hub/[HubID]/user’

#### Methods: 
-	GET
-	POST

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