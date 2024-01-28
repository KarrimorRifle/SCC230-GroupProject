import string as s
from random import choice

def genRandomID(length:int, ids:list[str]=[], prefix:str="", suffix:str="") -> list[str]:
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
        ids.append(genRandomID(length, ids, prefix, suffix))
    else:
        ids.append(randID)
    return ids