#Title:         iota/Schedule.py
#Desc:          File to hold the Schedule Class and related Functions
#               The Function of the Schedule Class is to run the user-defined code once a trigger is activated
#
#Last Update:   2024-2-11
#Updated By:    Kian Tomkins
#Interpreter:   Python 3.11

##IMPORTS##
from iota.Device import Device
from server import app

##CONSTANTS##
COMM_ELSE = "OTHERWISE"
COMM_FOR = "FOR"
COMM_IF = "IF"
COMM_SET = "SET"
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
                 code:list[FunctionCode] = [], isActive:bool=False, debug:bool=False):
        self.id = id
        self.name = name
        self.isPublic = isPublic
        if(isPublic):
            self.rating = rating
        self.isActive = isActive
        self.code = code
        
        self.devices = self.findDevices()
        self.variables = {}
        self.debug = debug

    ##PUBLIC METHODS##

    #Function loads data from DB into Schedule Object
    def loadfromdatabase(self, id:str):
        cursor = app.config['cursor']

        query = ("SELECT * FROM schedules "
                "WHERE ScheduleID = %s")
        cursor.execute(query, (id,))
        details = cursor.fetchone()

        if details is None:
            return 1

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
            for link in linkedCommands:
                if link['ParentID'] == block['BlockID']:
                    links.append(link['Link'])

            for param in params:
                if param['FunctionBlockID'] == block['BlockID']:
                    paramVals.append(param['Value'])

            funcBlock = FunctionCode(block['CommandType'], block['Num'], links ,paramVals)
            code.append(funcBlock)
            links = []
            paramVals = []
        
        return Schedule(id, details['ScheduleName'], details['IsPublic'], details['Rating'], code, details['IsActive'])

    #Runs the code to completion, and resets the values needed
    def runCode(self):
        i=0
        while i<len(self.code):
            #try:
                i=self.__translateSchedule(i)
            #except Exception as e:
            #    self.__addToErrorLog(e)
            #    break
        self.__resetCounts()
        self.variables = {}

    #Searches the schedule to find all instances of Devices being accessed
    def findDevices(self) -> list[Device]:
        #Find all the devices that the schedule uses. 
        return []

    #Initialises all the device
    def initDevices(self) -> dict[Device, bool]:
        #Checks if all the devices connected to the schedule can be accessed
        #Calls the functions to initiate connections. 
        pass
        
    ##PRIVATE METHODS##
    #Translates the schedule to actual code
    def __translateSchedule(self, index:int=0) -> int:
        self.isRunning=True

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
            case "OTHERWISE":
                #Value to check if all conditions for the else statement to be run are met
                allConditions=True

                #Checks if the if statement is correct, if the OTHERWISE statement is equal to an elif statement
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
                    print(f"{'OTHERWISE CONDITIONS NOT MET':<60}({self.id})")
                    
                #Returns the location of the end of the for loop, where the code should jump to next.
                return(self.__findEnd(index, self.code[index])+1)
            #Code for a set statement
            case "SET":
                if(self.debug):
                    #print response from set statement
                    pass
                exec(f"{evalParams[0]}={evalParams[1]}")

                #set a value of param 1 to param 2 (requires prereq devices working)
                self.code[index].hasRun+=1
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
    def __resolveVariable(self, variable:any) -> str:
        variable = str(variable)
        operators = ['<', '>', '<=', '>=', '==', '!=']

        if('.' in variable):
            variable = variable.split('.')
            #Checks if the variable passed in is a variable stored in the schedule
            if(variable[0] == 'var'):
                #checks if the variable already exists
                if(variable[1] not in self.variables.keys()):
                    self.variables.update({variable[1]:''})
                return f'self.variables["{variable[1]}"]'
            else:
                #checks if the variable passed is a valid device variable  
                for i in range(len(self.devices)):
                    if(variable[0] == self.devices[i].name and variable[1] in self.devices[i].data.keys()):
                        return f'self.devices[{i}].data["{variable[1]}"]'
        
        #checks if the variable is a number
        try:
            _v = float(variable)
        except:
            if(variable not in operators):
                return '"' + variable + '"'

        return str(variable)

    #Adds an error to a log in the database
    def __addToErrorLog(self, exception:str):
        #Email the user to let them know a schedule failed, with the reasons behind it.
        pass
