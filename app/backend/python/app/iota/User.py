#Title:         iota/User.py
#Desc:          File to hold the User Class and related Functions
#               The Function of the User Class is to hold information about users
#
#Last Update:   2024-3-13
#Updated By:    Aditya Khan
#Interpreter:   Python 3.11

##IMPORTS##
from server import app, addToErrorLog

##CLASS DEFINITIONS##
class User:
    ##VALUES##
    #id             Holds the ID for the user to be stored in the database
    #username       Holds the username that the user will see
    #email          Holds the email tied to the user's account
    #allowEmails    Whether or not the the user would like to recieve Emails. 
    #debug          Enables print statements for debugging purpose

    ##CONSTRUCTOR##
    def __init__(self, id:str, username:str, email:str,
                 allowEmails:bool=True, debug:bool=False):
        self.id = id
        self.username = username
        
        self.email = email
        self.allowEmails = allowEmails
        
        self.debug = debug
        if(debug):
            print(f"User Created With Values:\n"
                  f"id:\t\t{self.id}\n"
                  f"username:\t{self.username}\n"
                  f"email:\t\t{self.email}\n"
                  f"allowEmails:\t{self.allowEmails}\n")

##FUNCTION DEFINITIONS##
#Loads a User from the database
def loadUserFromDatabase(id:str) -> User:
    cursor = app.config['cursor']
    query = ("SELECT * FROM accounts "
                "WHERE AccountID = %s")

    cursor.execute(query, (id,))
    account = cursor.fetchone()

    return User(str(account['AccountID']), account['FirstName'], None, account['Email'])
