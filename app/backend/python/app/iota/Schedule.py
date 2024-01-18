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
    ##VALUES##
    #commandType    The type of command the code is, for translating to python i.e. IF, FOR, ELSE etc.
    #number         Which command of commandType the code is
    #name           The name of the command, to be used throughout the code
    #linkedCommands The commands it is linked to, i.e. which if statement an else statement is linked to
    #parameters     The parameters that the command takes
    #hasRun         Whether or not the command has run or not - useful for if/else statments

    def __init__(self, commandType:str, number:int, linkedCommands:[str]=None, parameters:[]=None):
        self.commandType = commandType
        self.number = number
        self.name = commandType+str(number)
        self.linkedCommands = linkedCommands
        self.parameters = parameters
        self.hasRun = False
    
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
def translateSchedule(code:[functionCode]):
    for i in range(code.length):
        match(code[i].commandType):
            case "FOR":
                for code[i].commandName in range (code[i].paramaters[0]):
                    pass
                    #Functionality to find end of loop and recursively execute code in loop.
            case "WHILE":
                while(eval(f"{code[i].paramaters[0]}{code[i].paramaters[1]}{code[i].paramaters[2]}")):
                      pass
                    #Functionality to find end of loop and recursively execute code in loop.
            case "IF":
                if(eval(f"{code[i].paramaters[0]}{code[i].paramaters[1]}{code[i].paramaters[2]}")):
                    pass
                    #Functionality to find end of if statement and recursively execute code in loop.
            case "OTHERWISE":
                if(code[i].paramaters.length == 0):
                    pass
                    #Find related functionCode and check if it has run
                else:
                    pass
                    #Find related functionCode and check if it has run then add parameters for elif statement
            case "SET":
                pass
                #set a value to param 2 (requires prereq devices working)
            case _:
                pass
