# Device Routes
## Refer back to iota classes as well for more information.

## Classes *for frontend to worry about by backend

### Device

Device model as handled by backend for database storing. The data in DB is processed slightly differently when handed to iota manager to create and use as a schedule class object. 

Structure shows variables and values for frontend to be familiar with.

#### Structure:
-	(string)DeviceID – Unique ID to identify specified Device
-	(string)DeviceName – Name of Device
-	(string)IpAddress – IP Address of Device
-	(string)Key – Device Key
-   (dict)Vars - All variables used by device
    -   Vars = { 'Name' : (string)varName, 'Type' : (string)varType, 'Access' : (int)Writeable}
        -   Writeable can be 0 or 1 for if user can update value of var
-   (float)Version - Version Num of Device
-   (string)Company - Company Device Belongs to
-	(string)HubID – ID of the Hub the device is linked to

## Routes

### ‘/hub/[HubID]/device'

#### Methods: 
-	GET
-	POST

#### Prerequisites: 
-	User Logged In
    -	Session ID Cookie set

#### GET: 

Lists ID, Name, Company of all devices that are linked to the hub with the given 'HubID'

##### Required Parameters:

##### Return Values:
List of dict objects contaning:
-	(string)DeviceID – Unique ID to identify specified Device
-	(string)DeviceName – Name of Device
-	(string)Company – Company Device Belongs to
-   (dict)Vars - All variables used by device
    -   Vars = { 'Name' : (string)varName, 'Type' : (string)varType, 'Access' : (int)Writeable}
        -   Writeable can be 0 or 1 for if user can update value of var

#### POST:

Creates new device in the database. HubID must be valid in URL.

##### Required Parameters:
-	(string)DeviceID – Unique ID to identify specified Device
-	(string)DeviceName – Name of Device
-	(string)IpAddress – IP Address of Device
-	(string)Key – Device Key
-   (float)Version - Version Num of Device
-   (string)Company - Company Device Belongs to

##### Return Values:
-	(string)DeviceID – Unique ID to identify specified Device

### ‘/hub/[HubID]/device/[DeviceID]’

#### Methods: 
-	GET
-	DELETE
-   PATCH

#### Prerequisites: 
-	User Logged In
    -	Session ID Cookie set

#### GET: 

Lists all values of specified device

##### Required Parameters:

##### Return Values:
dict object containing:
-	(string)DeviceID – Unique ID to identify specified Device
-	(string)DeviceName – Name of Device
-	(string)IpAddress – IP Address of Device
-	(string)Key – Device Key
-   (float)Version - Version Num of Device
-   (string)Company - Company Device Belongs to
-	(string)HubID – ID of the Hub the device is linked to
-   (dict)Vars - All variables used by device
    -   Vars = { 'Name' : (string)varName, 'Type' : (string)varType, 'Access' : (int)Writeable}
        -   Writeable can be 0 or 1 for if user can update value of var

#### DELETE:

Delete hub under ID of current user if has perms.

##### Required Parameters:

##### Return Values:
-	(string)DeviceID – Unique ID to identify specified Device

#### PATCH: 

Updates specified device data based on passed parameters if user has perms.

##### Optional Parameters:
-	(string)DeviceID – Unique ID to identify specified Device
-	(string)DeviceName – Name of Device
-	(string)IpAddress – IP Address of Device
-	(string)Key – Device Key
-   (float)Version - Version Num of Device
-   (string)Company - Company Device Belongs to

##### Return Values:
dict object containing updated values of:
-	(string)DeviceID – Unique ID to identify specified Device
-	(string)DeviceName – Name of Device
-	(string)IpAddress – IP Address of Device
-	(string)Key – Device Key
-   (float)Version - Version Num of Device
-   (string)Company - Company Device Belongs to
-	(string)HubID – ID of the Hub the device is linked to
-   (dict)Vars - All variables used by device
    -   Vars = { 'Name' : (string)varName, 'Type' : (string)varType, 'Access' : (int)Writeable}
        -   Writeable can be 0 or 1 for if user can update value of var