#Title:         iota/Hub.py
#Desc:          File to hold the Hub Class and related Functions
#               The Function of the Hub Class is to act as the bridge between Devices and their User 
#
#Last Update:   2024-1-27
#Updated By:    Kian Tomkins
#Interpreter:   Python 3.11

##IMPORTS##
from iota.Schedule import Schedule
from iota.User import User, loadUserFromDatabase
from server import app

##CLASS DEFINITION##
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
    def __init__(self, id: str, name: str, address: str="", logs:list[str]=[],
                 users:dict[User, int]={}, schedules: list[Schedule]=[], debug:bool=False):
        self.id = id
        self.name = name
        self.address = address
        self.logs = logs
        self.users=users
        self.schedules = schedules
        self.debug = debug

def loadFromDatabase(id:str) -> Hub:
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
        userDict[loadUserFromDatabase(user['AccountID'])] = user['PermissionLevel']

    return Hub(id=hub['HubID'], name=hub['HubName'], users=userDict)