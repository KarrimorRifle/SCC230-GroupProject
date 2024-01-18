##IMPORTS##
from iota.Trigger import Trigger
from iota.Device import Device

##CLASS DEFINITION##
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
    #functionCode   Holds the id for the function connected to the schedule

    ##CONSTRUCTOR##
    def __init__(self, id:str, name:str, rating:int=0, isPublic:bool=False,
                 triggers:Trigger=[None], devices:Device=[None], functionCode=None,
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
        self.functionCode = functionCode