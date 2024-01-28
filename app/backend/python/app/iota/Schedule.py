#Title:         iota/Schedule.py
#Desc:          File to hold the Schedule Class and related Functions
#               The Function of the Schedule Class is to run the user-defined code once a trigger is activated
#
#Last Update:   2024-1-27
#Updated By:    Kian Tomkins
#Interpreter:   Python 3.11

##IMPORTS##
from iota.Trigger import Trigger
from iota.Device import Device

##CLASS DEFINITIONS##
class FunctionCode():
    ##VALUES##
    #commandType    The type of command the code is, for translating to python i.e. IF, FOR, ELSE etc.
    #number         Which command of commandType the code is
    #name           The name of the command, to be used throughout the code
    #linkedCommands The commands it is linked to, i.e. which if statement an else statement is linked to
    #params         The parameters that the command takes
    #hasRun         Holds the number of times a FunctionCode has run

    ##CONSTRUCTOR##
    def __init__(self, commandType:str, number:int, linkedCommands:list=[], params:list[str]=[]):
        self.commandType = commandType
        self.number = number
        self.name = commandType+str(number)
        self.linkedCommands = linkedCommands
        self.params = params
        self.hasRun = 0
    
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
    #FunctionCode   Holds the untranslated code for a schedule
    #debug          Enables print statements for debugging purpose

    ##CONSTRUCTOR##
    def __init__(self, id:str, name:str, isPublic:bool=False, rating:int=1, triggers:list[Trigger]=[],
                 code:list[FunctionCode] = [], isActive:bool=False, debug:bool=False):
        self.id = id
        self.name = name
        self.isPublic = isPublic
        if(isPublic):
            self.rating = rating
        self.triggers = triggers
        self.isActive = isActive
        self.code = code
        self.devices = self.findDevices()
        self.debug = debug

    ##PUBLIC METHODS##
    #Translates the schedule to actual code
    def translateSchedule(self, index:int=0) -> int:
        if(self.debug):
            print(f"{self.code[index].commandType + ' ' + (' '.join(self.code[index].params)):<40}({self.id})")

        #Checks the type of statement that is at code[index]
        match(self.code[index].commandType):
            #Code for a for loop
            case "FOR":
                for i in range (self.code[index].params[0]):
                    self.code[index].hasRun+=1
                    self.__runConditional(index)

                #Returns the location of the end of the for loop, where the code should jump to next.
                return(self.__findEnd(index, self.code[index])+1)
            #Code for a while loop
            case "WHILE":
                while(eval(f"{' '.join(self.code[index].params)}")):
                    self.code[index].hasRun+=1
                    self.__runConditional(index)

                #Returns the location of the end of the for loop, where the code should jump to next.
                return(self.__findEnd(index, self.code[index])+1)
            #Code for an if statement
            case "IF":
                if(eval(f"{' '.join(self.code[index].params)}")):
                    self.code[index].hasRun+=1
                    self.__runConditional(index)
                elif(self.debug):
                    print(f"{'IF CONDITIONS NOT MET':<40}({self.id})")
                    
                #Returns the location of the end of the for loop, where the code should jump to next.
                return(self.__findEnd(index, self.code[index])+1)
            #Code for an else/else if statement
            case "OTHERWISE":
                #Value to check if all conditions for the else statement to be run are met
                allConditions=True

                #Checks if the if statement is correct, if the OTHERWISE statement is equal to an elif statement
                if(len(self.code[index].params) != 0):
                    if(not(eval(f"{' '.join(self.code[index].params)}"))):
                        allConditions=False
                #Checks if any of the linked if and elif statements ran
                for i in range (len(self.code[index].linkedCommands)):
                    if(self.code[index].linkedCommands[i].hasRun>0):
                        allConditions=False
                    break
                #Runs the code if all the checks pass
                if(allConditions):

                    self.code[index].hasRun+=1
                    self.__runConditional(index)

                elif(self.debug):
                        print(f"{'OTHERWISE CONDITIONS NOT MET':<40}({self.id})")
                    
                #Returns the location of the end of the for loop, where the code should jump to next.
                return(self.__findEnd(index, self.code[index])+1)
            #Code for a set statement
            case "SET":
                if(self.debug):
                    #print response from set statement
                    pass

                #set a value of param 1 to param 2 (requires prereq devices working)
                self.code[index].hasRun+=1
                return index+1
            case "GET":
                if(self.debug):
                    #print get statement
                    pass

                #get value of param 1 (requires prereq devices working)
                self.code[index].hasRun+=1
                return index+1
            #Default case to ignore End or invalid statements
            case _:
                return index+1

    def findDevices(self) -> list[Device]:
        #Find all the devices that the schedule uses. 
        return []

    def initDevices(self) -> dict[Device, bool]:
        #Checks if all the devices connected to the schedule can be accessed
        #Calls the functions to initiate connections. 
        pass
        
    ##PRIVATE METHODS##
    #Runs all the lines in a condition statement or loop
    def __runConditional(self, index:int):
        if(self.debug):
            print(f"{'RUN CONDITIONAL':<40}({self.id})")

        #Creates a temporary index to run the required commands
        _index=index
        #Loops through every statement until the end statement
        while(_index != self.__findEnd(index, self.code[index])):
            _index+=1
            self.translateSchedule(index=_index)

    #Finds the end of a conditional statement or loop
    def __findEnd(self, index:int, statement:FunctionCode) -> int:
        while(self.code[index].commandType!="END" and not (statement.name in self.code[index].linkedCommands)):
            index+=1

        return index

    def __warnUser(self):
        #Email the user to let them know a schedule failed, with the reasons behind it.
        pass
