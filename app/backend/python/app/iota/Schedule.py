#Interpreter:   Python 3.11

##IMPORTS##
from iota.Device import Device

##CONSTANTS##
	@@ -21,8 +20,7 @@
class FunctionCode():
    ##VALUES##
    #commandType    The type of command the code is, for translating to python i.e. IF, FOR, ELSE etc.
    #number         Effectively the line number the code is at
    #linkedCommands The commands it is linked to, i.e. which if statement an else statement is linked to
    #params         The parameters that the command takes
    #hasRun         Holds the number of times a FunctionCode has run
	@@ -33,6 +31,7 @@ def __init__(self, commandType:str, number:int, linkedCommands:list=[int], param
        self.number = number
        self.linkedCommands = linkedCommands
        self.params = params

        self.hasRun = 0

class Schedule:
	@@ -51,16 +50,15 @@ class Schedule:

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
	@@ -100,33 +98,41 @@ def __translateSchedule(self, index:int=0) -> int:
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
	@@ -141,15 +147,15 @@ def __translateSchedule(self, index:int=0) -> int:
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
	@@ -171,7 +177,7 @@ def __translateSchedule(self, index:int=0) -> int:
    #Runs all the lines in a condition statement or loop
    def __runConditional(self, index:int):
        if(self.debug):
            print(f"{'RUN CONDITIONAL':<60}({self.id})")

        #Creates a temporary index to run the required commands
        _index=index
	@@ -184,10 +190,11 @@ def __runConditional(self, index:int):
    def __findEnd(self, index:int, statement:FunctionCode) -> int:
        while(not(self.code[index].commandType=="END" and (statement.number in self.code[index].linkedCommands))):
            index+=1
        return index




    #Resets the number of times a piece of code has run for future schedules
    def __resetCounts(self):
        self.isRunning = False
	@@ -196,7 +203,8 @@ def __resetCounts(self):
            self.code[i].hasRun = 0

    #Changes an instance of a value to an evaluable format
    def __resolveVariable(self, variable:any) -> str:
        variable = str(variable)
        operators = ['<', '>', '<=', '>=', '==', '!=']

        if('.' in variable):
	@@ -217,22 +225,12 @@ def __resolveVariable(self, variable:str) -> str:
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

def loadFromDatabase(id:str) -> Schedule:
    pass
