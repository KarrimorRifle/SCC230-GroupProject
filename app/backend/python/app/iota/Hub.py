#Title:         iota/Hub.py
#Desc:          File to hold the Hub Class and related Functions
#               The Function of the Hub Class is to act as the bridge between Devices and their User 
#
#Last Update:   2024-3-13
#Updated By:    Kian Tomkins
#Interpreter:   Python 3.11

##IMPORTS##
from iota.Schedule import Schedule
from iota.User import *
from server import app, addToErrorLog

##CLASS DEFINITIONS##
class Hub:
    ##VALUES##
    #id         Holds the ID for the hub to be stored in the database
    #name       Holds the name the user will see for the hub
    #address    Holds the address that is tied to the hub
    #users      Holds the users that are on the hub and their permission levels
    #logs       Holds the previous actions of the hub
    #schedules  Holds the schedules that the hub is a part of
    #debug      Enables print statements for debugging purpose

    ##CONSTRUCTOR##
    def __init__(self, id:str, name:str, address:str="", logs:list[str]=[],
                 users:dict[str, int]={}, schedules:list[Schedule]=[], debug:bool=False):
        self.debug = debug
        
        self.id = id
        self.name = name

        self.address = address
        
        self.logs = logs
        
        self.users=users
        self.schedules = schedules
        
        if(debug):
            print(f"Hub Created With Values:\n"
                  f"id:\t\t{self.id}\n"
                  f"name:\t\t{self.name}\n"
                  f"address:\t{self.address}\n"
                  f"logs:\t\t{str(self.logs)[:77]}...\n"
                  f"users:\t\t{str(self.users)[:77]}...\n"
                  f"schedules:\t{str(self.schedules)[:77]}...\n")

##FUNCTION DEFINITIONS##
#Loads a Hub from the database
def loadHubFromDatabase(id:str) -> Hub:
    cursor = app.config['cursor']
    query = ("SELECT * FROM hubs WHERE HubID = %s")
    cursor.execute(query, (id,))
    hub = cursor.fetchone()

    if hub is None:
        return None
    
    query = ("SELECT AccountID, PermissionLevel FROM accounts_hubsRelation WHERE HubID = %s")
    cursor.execute(query, (id,))
    users = cursor.fetchall()
    userDict = {}
    for user in users:
        userDict[user['AccountID']] = user['PermissionLevel']

    return Hub(id=hub['HubID'], name=hub['HubName'], users=userDict)
