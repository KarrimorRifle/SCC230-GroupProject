# Device Routes
## Refer back to iota classes as well for more information.

## Classes *for frontend to worry about by backend

### Device

Device model as handled by backend for database storing. The data in DB is processed slightly differently when handed to iota manager to create and use as a schedule class object. 

Structure shows variables and values for frontend to be familiar with.

#### Structure:
-	(string)DeviceID – Unique ID to identify specified Device
-	(string)DeviceName – Name of Device
-	(string)DeviceType – Physical type of Device
-	(string)IpAddress – IP Address of Device
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

Lists ID, Name, Type of all devices that are linked to the hub with the given 'HubID'

##### Required Parameters:

##### Return Values:
List of dict objects contaning:
-	(string)DeviceID – Unique ID to identify specified Device
-	(string)DeviceName – Name of Device
-	(string)DeviceType – Physical type of Device

#### POST:

Creates new device in the database.

##### Required Parameters:
-	(string)DeviceName – Name of Device
-	(string)DeviceType – Physical type of Device
-	(string)IpAddress – IP Address of Device

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

Lists ID, Name, Type, IP address, hub ID of specified device

##### Required Parameters:

##### Return Values:
dict object containing:
-	(string)DeviceID – Unique ID to identify specified Device
-	(string)DeviceName – Name of Device
-	(string)DeviceType – Physical type of Device
-	(string)IpAddress – IP Address of Device
-	(string)HubID – ID of the Hub the device is linked to

#### DELETE:

Delete hub under ID of current user if has perms.

##### Required Parameters:

##### Return Values:
-	(string)DeviceID – Unique ID to identify specified Device

#### PATCH: 

Updates specified device data based on passed parameters if user has perms.

##### Optional Parameters:
-	(string)DeviceName – Name of Device
-	(string)DeviceType – Physical type of Device
-	(string)IpAddress – IP Address of Device
-	(string)HubID – ID of the Hub the device is linked to

##### Return Values:
dict object containing updated values of:
-	(string)DeviceID – Unique ID to identify specified Device
-	(string)DeviceName – Name of Device
-	(string)DeviceType – Physical type of Device
-	(string)IpAddress – IP Address of Device
-	(string)HubID – ID of the Hub the device is linked to