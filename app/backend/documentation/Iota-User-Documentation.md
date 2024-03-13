# [Backend/Python/App/Iota/User.py](../python/app/iota/User.py)
# Required Modules
## server
[Documentation]()\
[File](../python/app/server.py)

# Classes
## User
### Description
---
Class to hold information about the users for the user interface.

### Values
---
- (str) id - The unique ID for the User.
- (str) username - The name the user has chosen 
- (str) email - The User's email
- (bool) allowEmails - Whether or not the user has notification emails
- (bool) debug - Whether the class should print statements for debugging

### Constructor
---
**Required Parameters**
- (str) id - the value the object’s id variable is set to.
- (str) username - the value the object’s username variable is set to.
- (str) email - the value the object’s email variable is set to.

**Optional Parameters**
- (bool) allowEmails - the value the object’s allowEmails variable is set to.
- (bool) debug - the value the object’s debug variable is set to.

---
# Functions
- ***loadUserFromDatabase(id)***\
  **Description**\
  Loads a User from the database, based on it's ID
  
  **Required Parameters**
  - (str) id - The ID of the User that is being retrieved.
  
  **Return Value**\
  (User) The User retrieved from the database
---