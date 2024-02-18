#Title:         iota/__init__.py
#Desc:          File to initialise the IOTA module and hold general functions
#
#Last Update:   2024-2-4
#Updated By:    Kian Tomkins
#Interpreter:   Python 3.11

import string as s
from random import choice

def genRandomID(length:int=16, ids:list[str]=[], prefix:str="", suffix:str="") -> list[str]:
    #Create the ID
    chars=s.ascii_letters+s.digits
    randID= prefix + ''.join(choice(chars) for _ in range(length)) + suffix

    #Iterates through the list of IDs to ensure it is unique    
    exists=False

    for i in range(len(ids)):
        if(randID == ids[i]):
            exists = True
            break
    if(exists):
        return(genRandomID(length, ids, prefix, suffix))
    return(randID)