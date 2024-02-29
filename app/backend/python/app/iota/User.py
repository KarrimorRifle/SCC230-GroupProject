#Title:         iota/User.py
#Desc:          File to hold the User Class and related Functions
#               The Function of the User Class is to hold information about users
#
#Last Update:   2024-2-21
#Updated By:    Aditya Khan
#Interpreter:   Python 3.11

##IMPORTS##
from iota.Device import Device
from iota import genRandomID

from server import app

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

# Function creates User object based on User data in DB
def loadUserFromDatabase(id:str) -> User:
    cursor = app.config['cursor']
    query = ("SELECT * FROM accounts "
                "WHERE AccountID = %s")

    cursor.execute(query, (id,))
    account = cursor.fetchone()

    return User(str(account['AccountID']), account['FirstName'], None, account['Email'])
