#Title:         iota/__init__.py
#Desc:          File to initialise the IOTA module and hold general functions
#
#Last Update:   2024-2-15
#Updated By:    Kian Tomkins
#Interpreter:   Python 3.11

import string as s
from random import choice
from flask import current_app

TABLE_API = 'apis'
TABLE_DEV = 'devices'
TABLE_HUB = 'hubs'
TABLE_SCH = 'schedules'
TABLE_TRG = 'triggers'
TABLE_USR = 'accounts'
TABLES = [TABLE_API, TABLE_DEV, TABLE_DEV, 
          TABLE_HUB, TABLE_SCH, TABLE_TRG, TABLE_USR]

DEFAULT_PREFIX = {
    'apis' : 'API-',
    'devices' : 'DEV-',
    'hubs' : 'HUB-',
    'schedules' : 'SCH-',
    'triggers' : 'TRG-',
    'accounts' : 'USR-'
}

#Creates a random ID
def genRandomID(length:int=16, ids:list[str]=[], prefix:str="", suffix:str="") -> list[str]:
    #Create the ID
    chars=s.ascii_letters+s.digits
    randID= prefix + ''.join(choice(chars) for _ in range(length-len(prefix)))

    return(randID)

#Checks if the ID is in the Database
def __checkIfIDExists(id:str, table:str) -> bool:
    cursor = current_app.config['cursor']
    connection= current_app.config['connection']
    query = ("SELECT %sID FROM %s "
                "WHERE AccountID = %s")

    cursor.execute(query, (table, table, id))
    print(cursor.fetchone())
    return True

#Creates a new, unique ID
def getID(table:str, length:int=16, prefix:str=""):
    if (table not in TABLES):
        print("INVALID TABLE")
        return None
    else:
        if(prefix == ""):
            prefix = DEFAULT_PREFIX[table]
        newID = __genRandomID(length, prefix)
        while(not(__checkIfIDExists(newID, table))):
            newID = __genRandomID(length, prefix)
        return newID

print(getID(table=TABLE_SCH))
