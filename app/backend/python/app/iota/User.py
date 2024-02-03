#Title:         iota/User.py
#Desc:          File to hold the User Class and related Functions
#               The Function of the User Class is to hold information about users
#
#Last Update:   2024-1-27
#Updated By:    Kian Tomkins
#Interpreter:   Python 3.11

##IMPORTS##
from iota.Device import Device
from iota import genRandomID

##CLASS DEFINITION##
class User:
    ##VALUES##
    #id             Holds the ID for the user to be stored in the database
    #username       Holds the username that the user will see
    #password       Holds the password which the user will need to access their account
    #email          Holds the email tied to the user's account
    #allowEmails    Whether or not the the user would like to recieve Emails. 
    #debug          Enables print statements for debugging purpose

    ##CONSTRUCTOR##
    def __init__(self, id:str, username:str, password:str, email:str,
                 allowEmails:bool=True, debug:bool=False):
        self.id = id
        self.username=username
        self.password=password
        self.email=email
        self.allowEmails = allowEmails
        self.debug = debug