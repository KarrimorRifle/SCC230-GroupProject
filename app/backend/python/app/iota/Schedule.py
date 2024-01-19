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
    #commandType    The type of command the code is, for translating to python index.e. IF, FOR, ELSE etc.
    #number         Which command of commandType the code is
    #name           The name of the command, to be used throughout the code
    #linkedCommands The commands it is linked to, index.e. which if statement an else statement is linked to
    #params         The params that the command takes
    #hasRun         Whether or not the command has run or not - useful for if/else statments

    def __init__(self, commandType:str, number:int, linkedCommands:[str]=[], params:list=[]):
        self.commandType = commandType
        self.number = number
        self.name = commandType+str(number)
        self.linkedCommands = linkedCommands
        self.params = params
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
                 triggers:[Trigger]=[], devices:[Device]=[], code:[functionCode] = [],
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


#Finds the end of a conditional statement or loop
def findEnd(code:[functionCode], index:int, statement:functionCode):
    while(code[index].commandType!="END" and not (statement.name in code[index].linkedCommands)):
        index+=1
    return index

#Runs all the lines in a condition statement or loop
def runConditional(code:[functionCode], index:int):
    #Creates a temporary index to run the required commands
    _index=index
    #Loops through every statement until the end statement
    while(_index != findEnd(code,index,code[index])):
        _index+=1
        translateSchedule(code=code, index=_index)
        

#Translates the schedule to actual code
def translateSchedule(code:[functionCode], index:int=0):
    #Checks the type of statement that is at code[index]
    match(code[index].commandType):
        #Code for a for loop
        case "FOR":
            for i in range (code[index].params[0]):
                code[index].hasRun=True
                runConditional(code, index)

            #Returns the location of the end of the for loop, where the code should jump to next.
            return(findEnd(code,index,code[index]))
        #Code for a while loop
        case "WHILE":
            while(eval(f"{' '.join(code[index].params)}")):
                code[index].hasRun=True
                runConditional(code, index)

            #Returns the location of the end of the for loop, where the code should jump to next.
            return(findEnd(code,index,code[index]))
        #Code for an if statement
        case "IF":
            if(eval(f"{' '.join(code[index].params)}")):
                code[index].hasRun=True
                runConditional(code, index)
                
            #Returns the location of the end of the for loop, where the code should jump to next.
            return(findEnd(code,index,code[index]))
        #Code for an else/else if statement
        case "OTHERWISE":
            #Value to check if all conditions for the else statement to be run are met
            allConditions=True

            #Checks if the if statement is correct, if the OTHERWISE statement is equal to an elif statement
            if(len(code[index].params) != 0):
                if(not(eval(f"{' '.join(code[index].params)}"))):
                    allConditions=False
            #Checks if any of the linked if and elif statements ran
            for i in range (len(code[index].linkedCommands)):
                if(code[index].linkedCommands[i].hasRun):
                   allConditions=False
                   break
            
            if(allConditions):
                code[index].hasRun=True
                runConditional(code, index)

            #Returns the location of the end of the for loop, where the code should jump to next.
            return(findEnd(code,index,code[index]))
        #Code for a set statement
        case "SET":
            print(code[index].params[0])
            code[index].hasRun=True
            return index+1
            #set a value to param 2 (requires prereq devices working)
        #Default case to ignore End or invalid statements
        case _:
            pass
