#Title:         iota/Schedule.py
#Desc:          File to hold the Schedule Class and related Functions
#               The Function of the Schedule Class is to run the user-defined code once a trigger is activated
#
#Last Update:   2024-2-29
#Updated By:    Kian Tomkins
#Interpreter:   Python 3.11

##IMPORTS##
from iota.Device import *
import time
import threading
from server import app

##CONSTANTS##
COMM_ELSE = "ELSE"
COMM_FOR = "FOR"
COMM_IF = "IF"
COMM_SET = "SET"
COMM_WAIT = "WAIT"
COMM_WHILE = "WHILE"


##CLASS DEFINITIONS##
class FunctionCode():
    ##VALUES##
    #commandType    The type of command the code is, for translating to python i.e. IF, FOR, ELSE etc.
    #number         Effectively the line number the code is at
    #linkedCommands The commands it is linked to, i.e. which if statement an else statement is linked to
    #params         The parameters that the command takes
    #hasRun         Holds the number of times a FunctionCode has run

    ##CONSTRUCTOR##
    def __init__(self, commandType:str, number:int, linkedCommands:list=[int], params:list[str]=[]):
        self.commandType = commandType
        self.number = number
        self.linkedCommands = linkedCommands
        self.params = params

        self.hasRun = 0

class Schedule:
    ##VALUES##
    #id         Holds the ID for the schedule to be stored in the database
    #name       Holds the name that the user will see for the schedule
    #isPublic   Checks if the schedule is in the open source page
    #rating     Holds the sum of the ratings left by other users 
    #triggers   Holds the triggers that will activate the schedule
    #code       Holds the untranslated code for a schedule
    #devices    Holds the devices linked to the schedule
    #variables  Holds the variables used throughout the code
    #isRunning  Checks if the schedule is currently running
    #isActive   Checks if the schedule is currently able to run
    #debug      Enables print statements for debugging purpose

    ##CONSTRUCTOR##
    def __init__(self, id:str, name:str, isPublic:bool=False, rating:int=1, 
                 code:list[FunctionCode] = [], isActive:bool=True, debug:bool=False):
        self.id = id
        self.name = name
        self.isPublic = isPublic
        if(isPublic):
            self.rating = rating

        self.isActive = isActive
        self.isRunning = False
        self.code = code
    
        self.variables ={}
        self.devices = self.findDevices()
        self.debug = debug

    ##PUBLIC METHODS##
    #Runs the code to completion, and resets the values needed
    def runCode(self):
        def runThread():
            self.isRunning = True
            i = 0
            while i < len(self.code):
                try:
                    i = self.__translateSchedule(i)
                except Exception as e:
                    if(self.debug):
                        print(e)
                    self.__addToErrorLog(e)
                    break
            self.__resetCounts()
            self.variables = {}
            self.isRunning = False
          
        #Check if the code is already running
        if(not(self.isRunning) and self.isActive):
            # Start a new thread to execute the code
            thread = threading.Thread(target=runThread)
            thread.start()

    #Searches the schedule to find all instances of Devices being accessed
    def findDevices(self) -> list[Device]:
        devices = []
        for i in range(len(self.code)):
            for j in range(len(self.code[i].params)):
                var = self.__resolveVariable(self.code[i].params[j])
                if(type(var)==str):
                    var.split('.')
                    newDevice = loadDeviceFromDatabase(var[0])
                    if(newDevice != None):
                        devices.append(newDevice)
        return devices
        
    ##PRIVATE METHODS##
    #Translates the schedule to actual code
    def __translateSchedule(self, index:int=0) -> int:
        #evaluates all the parameters
        evalParams = []
        for i in range(len(self.code[index].params)):
            evalParams.append(self.__resolveVariable(self.code[index].params[i]))

        if(self.debug):
            print(f"{self.code[index].commandType + ' ' + (' '.join(evalParams)):<60}({self.id})")

        #Checks the type of statement that is at code[index]
        match(self.code[index].commandType):
            #Code for a for loop
            case "FOR":
                for i in range (eval(evalParams[0])):
                    self.code[index].hasRun+=1

                    #Creates an iterator variable for the current loop
                    self.variables[f"i{self.code[index].number}"] = self.code[index].hasRun
                    
                    self.__runConditional(index)

                #Returns the location of the end of the for loop, where the code should jump to next.
                return(self.__findEnd(index, self.code[index])+1)
            #Code for a while loop
            case "WHILE":                
                while(eval(f"{' '.join(evalParams)}")):
                    self.code[index].hasRun+=1

                    #Creates an iterator variable for the current loop
                    self.variables[f"i{self.code[index].number}"] = self.code[index].hasRun
                    
                    self.__runConditional(index)

                #Returns the location of the end of the for loop, where the code should jump to next.
                return(self.__findEnd(index, self.code[index])+1)
            #Code for an if statement
            case "IF":
                if(eval(f"{' '.join(evalParams)}")):
                    self.code[index].hasRun+=1
                    self.__runConditional(index)
                elif(self.debug):
                    print(f"{'IF CONDITIONS NOT MET':<60}({self.id})")
                    
                #Returns the location of the end of the for loop, where the code should jump to next.
                return(self.__findEnd(index, self.code[index])+1)
            #Code for an else/else if statement
            case "ELSE":
                #Value to check if all conditions for the else statement to be run are met
                allConditions=True

                #Checks if the if statement is correct, if the ELSE statement is equal to an elif statement
                if(len(evalParams) != 0):
                    if(not(eval(f"{' '.join(evalParams)}"))):
                        allConditions=False
                #Checks if any of the linked if and elif statements ran
                for i in range (len(self.code[index].linkedCommands)):
                    if(self.code[self.code[index].linkedCommands[i-1]].hasRun>0):
                        allConditions=False
                        break
                #Runs the code if all the checks pass
                if(allConditions):
                    self.code[index].hasRun+=1
                    self.__runConditional(index)
                elif(self.debug):
                    print(f"{'ELSE CONDITIONS NOT MET':<60}({self.id})")
                    
                #Returns the location of the end of the for loop, where the code should jump to next.
                return(self.__findEnd(index, self.code[index])+1)
            #Code for a set statement
            case "SET":
                if(self.debug):
                    #print response from set statement
                    pass
                exec(f"{' '.join(evalParams)}")

                #set a value of param 1 to param 2 (requires prereq devices working)
                self.code[index].hasRun+=1
                return index+1
            case "WAIT":
                #Code to make the current thread sleep
                time.sleep(evalParams[0])
                return index+1
            #Default case to ignore End or invalid statements
            case _:
                return index+1

    #Runs all the lines in a condition statement or loop
    def __runConditional(self, index:int):
        if(self.debug):
            print(f"{'RUN CONDITIONAL':<60}({self.id})")

        #Creates a temporary index to run the required commands
        _index=index
        #Loops through every statement until the end statement
        while(_index != self.__findEnd(index, self.code[index])):
            _index+=1
            self.__translateSchedule(index=_index)

    #Finds the end of a conditional statement or loop
    def __findEnd(self, index:int, statement:FunctionCode) -> int:
        while(not(self.code[index].commandType=="END" and (statement.number in self.code[index].linkedCommands))):
            index+=1
        return index
    
    #Resets the number of times a piece of code has run for future schedules
    def __resetCounts(self):
        self.isRunning = False

        for i in range(len(self.code)):
            self.code[i].hasRun = 0

    #Changes an instance of a value to an evaluable format
   #Changes an instance of a value to an evaluable format
    def __resolveVariable(self, variable:str) -> str:
        variable = str(variable)
        if(len(variable) == 0):
            return '""'

        operators = ['<', '>', '<=', '>=', '==', '!=', # logic operators
                     '+', '-', '=', '/', '*', '%' # assignment operators
                     '+=' '-=', '/=', '*='] # self-assignment operators
        
        #checks if the variable is a number
        try:
            _v = float(variable)
            return variable
        except:
            if('.' in variable):
                sVariable = variable.split('.')
                #Checks if the variable passed in is a variable stored in the schedule
                if(sVariable[0] == 'var'):
                    #checks if the variable already exists
                    if(sVariable[1] not in self.variables.keys()):
                        self.variables.update({sVariable[1]:''})
                    return f'self.variables["{sVariable[1]}"]'
                else:
                    #checks if the variable passed is a valid device variable  
                    for i in range(len(self.devices)):
                        if(sVariable[0] == self.devices[i].name and sVariable[1] in self.devices[i].data.keys()):
                            return f'self.devices[{i}].data["{sVariable[1]}"]'
        
        #Checks if the variable is an operator
        if(variable not in operators):
            #Checks if the variable is already in quotations
            if(variable[0] == '"' or variable[0] == "'"):
                variable[0] = ""
            if(variable[-1] == '"' or variable[-1] == "'"):
                variable[-1] = "" 
        #returns the string
        return str(variable)

    #Adds an error to a log in the database
    def __addToErrorLog(self, exception:str):
        #Email the user to let them know a schedule failed, with the reasons behind it.
        pass

def loadScheduleFromDatabase(id:str) -> Schedule:
    cursor = app.config['cursor']
    query = ("SELECT * FROM schedules "
             "WHERE ScheduleID = %s")
    cursor.execute(query, (id,))
    details = cursor.fetchone()

    if details is None:
        return None

    query = ("SELECT * FROM function_blocks "
             "WHERE ScheduleID = %s")
    cursor.execute(query, (id,))
    functionBlocks = cursor.fetchall()

    code = []

    query = ("SELECT Link, ParentID FROM function_block_links "
             "WHERE ScheduleID = %s")
    cursor.execute(query, (id,))
    linkedCommands = cursor.fetchall()
    linkedCommands = [link for link in linkedCommands]

    query = ("SELECT Value, FunctionBlockID, ListPos FROM function_block_params "
             "WHERE ScheduleID = %s")
    cursor.execute(query, (id,))
    params = cursor.fetchall()
    params = [param for param in params]
    params = sorted(params, key=lambda x: x['ListPos'])

    links = []
    paramVals = []
    for block in functionBlocks:
        if linkedCommands is None:
            links = None
        else:
            for link in linkedCommands:
                if link['ParentID'] == block['BlockID']:
                    links.append(link['Link'])

        if params is None:
            paramVals = None
        else:
            for param in params:
                if param['FunctionBlockID'] == block['BlockID']:
                    paramVals.append(param['Value'])

        funcBlock = FunctionCode(block['CommandType'], block['Num'], links ,paramVals)
        code.append(funcBlock)
        links = []
        paramVals = []
        
    return Schedule(id, details['ScheduleName'], details['IsPublic'], details['Rating'], code, details['IsActive'])
