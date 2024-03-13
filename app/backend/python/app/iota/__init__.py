#Title:         iota/__init__.py
#Desc:          File to initialise the IOTA module and hold general functions
#
#Last Update:   2024-3-13
#Updated By:    Kian Tomkins
#Interpreter:   Python 3.11

##IMPORTS##
import string as s
from random import choice

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
