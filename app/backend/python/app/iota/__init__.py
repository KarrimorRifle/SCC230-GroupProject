#Title:         iota/__init__.py
#Desc:          File to initialise the IOTA module and hold general functions
#
#Last Update:   2024-3-13
#Updated By:    Kian Tomkins
#Interpreter:   Python 3.11

##IMPORTS##
import string as s
from random import choice
from server import app
from datetime import datetime, UTC

##FUNCTION DEFINITIONS##
#Generates a random ID for the database to use
def genRandomID(length:int=16, ids:list[str]=[], prefix:str="", suffix:str="", debug:bool=False) -> list[str]:
    #Create the ID
    chars=s.ascii_letters+s.digits
    randID= prefix + ''.join(choice(chars) for _ in range(length)) + suffix

    #Iterates through the list of IDs to ensure it is unique    
    exists=False

    for i in range(len(ids)):
        if(randID == ids[i]):
            exists = True
            break
    #If the ID already exists, it runs genRandomID until a unique one is generated
    if(exists):
        if(debug):
            print(f"ID '{randID}' Already Exists")
        return(genRandomID(length, ids, prefix, suffix, debug))
    
    if(debug):
        print(f"ID '{randID}' Created.")
    return(randID)

#Adds an error to the error log in the database
def addToErrorLog(exception:str):
    cursor = app.config['cursor']
    timestamp = datetime.strftime(datetime.now(UTC), "%Y-%m-%d %H-%M-%S")
    query = ("INSERT INTO error_log (Error, Time)"
             f"VALUES ('{exception}', '{timestamp}')")
    cursor.execute(query)
