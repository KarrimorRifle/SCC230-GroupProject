# Title:    main.py
# Desc:     program to run and the the other classes.
# 
# Last Updated: 20/12/23
# Updated by:   Kian Tomkins
# Interpreter:  Python 3.11

##IMPORTS##
from iota.User import User
##GLOBAL VARIABLES##

##FUNCTION DEFINITIONS##
def main():
    testUser = User(id="TEST0000",username="Kain",password="Pass123")
    print(testUser.username)

##MAIN CALL##
main()