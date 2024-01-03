##IMPORTS##
import json

#CLASS DEFINITION#
class Trigger:
    ##VALUES##
    #id     Holds the id to store the Trigger in the database
    #name   Holds the name that the user will see
    #data   Holds the data that is needed to set off the trigger

    ##CONSTRUCTOR##
    def __init__(self, id:str, name:str, data:dict={None:None}):
        self.id = id
        self.name = name
        self.data = data