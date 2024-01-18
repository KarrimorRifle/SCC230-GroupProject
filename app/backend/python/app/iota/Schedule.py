#Title:         iota/Schedule.py
#Desc:          File to hold the Schedule Class and related Functions
#               The Function of the Schedule Class is to run the user-defined code once a trigger is activated
#
#Last Update:   2024-1-18
#Updated By:    Kian Tomkins
#Interpreter:   Python 3.11

##IMPORTS##
from iota.Trigger import Trigger
from iota.Device import Device

##CLASS DEFINITIONS##
class functionCode():
    def __init__(self, commandType:str, commandNo:int, linkedCommands:str = None, parameters:[]=None):
        self.commandType = commandType
        self.commandID = commandNo
        self.commandName = commandType+str(commandNo)
        self.linkedCommands = linkedCommands
        self.parameters = parameters
    
class Schedule:
    ##VALUES##
    #id             Holds the ID for the schedule to be stored in the database
    #name           Holds the name that the user will see for the schedule
    #isPublic       Checks if the schedule is in the open source page
    #rating         Holds the sum of the ratings left by other users 
    #trigger        Holds the triggers that will activate the schedule
    #devices        Holds the devices linked to the schedule
    #isRunning      Checks if the schedule is currently running
    #isActive       Checks if the schedule is currently able to run
    #functionCode   Holds the untranslated code for a schedule

    ##CONSTRUCTOR##
    def __init__(self, id:str, name:str, rating:int=0, isPublic:bool=False,
                 triggers:Trigger=[None], devices:Device=[None], code:[functionCode] = None,
                 isRunning:bool=False, isActive:bool=False):
        self.id = id
        self.name = name
        self.isPublic = isPublic
        if(isPublic):
            self.rating = rating
        self.triggers = triggers
        self.devices = devices
        self.isRunning = isRunning
        self.isActive = isActive
        self.code = code

#Translates the schedule to actual code
def translateSchedule(code):
    for i in range(code[0].length):
        match((code[0][i][0]).upper):
            case "FOR":
                print()
            case "WHILE":
                print()
            case "IF":
               print()
            case "OTHERWISE":
                print()
            case "END":
                print()
            case "SET":
                print()