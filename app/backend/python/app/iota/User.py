##IMPORTS##
from iota.Hub import Hub
from iota.Schedule import Schedule

##CLASS DEFINITION##
class User:
    ##VALUES##
    #id             Holds the ID for the user to be stored in the database
    #username       Holds the username that the user will see
    #password       Holds the password which the user will need to access their account
    #email          Holds the email tied to the user's account
    #houseRoles     Holds the user's homes and their permission level within them (User:int)
    #schedules      Holds the schedules the user has saved

    ##CONSTRUCTOR##
    def __init__(self, id:str, username:str, password:str, email:str="",
                 houseRoles:dict={None:0}, schedules:Schedule=[None]):
        self.id = id
        self.username=username
        self.password=password
        self.email=email
        self.houseRoles = houseRoles
        self.schedules = schedules