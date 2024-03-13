# [Backend/Python/App/Iota/\_\_init__.py](../python/app/iota/__init__.py)
# Required Modules
## random
[Documentation](https://docs.python.org/3/library/random.html)

## string
[Documentation](https://docs.python.org/3/library/string.html)

# Functions
- ***genRandomID(length, ids, prefix, suffix)***\
  **Description**\
  Generates a random, unique ID, for Objects in the database 

  **Optional Parameters**
  - (int) - length - The length that the generated string should be\
  Default Value: 16
  - ([str]) - ids - The list of already existing IDs\
  Default Value: []
  - (str) - prefix - The prefix that the ID should start with\
  Default Value: ""
  - (str) - suffix - The suffix that the ID should end with\
  Default Value: ""

  **Return Value**\
  (str) The ID that is generated.

---
- ***addToErrorLog(self, exception)***\
  **Description**
  Adds caught errors to a log in the database. If the user has email updates on, this function emails the user, warning them if a schedule is unable to run.
  
  **Required Parameters**
  - (str) error message - the error that is being added to the log
---