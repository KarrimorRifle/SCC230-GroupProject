#Title:         iota/Api.py
#Desc:          File to hold the Api Class and related Functions
#               The Function of the Api Class is to define the method to communicate with IOT Devices
#
#Last Update:   2024-1-18
#Updated By:    Kian Tomkins
#Interpreter:   Python 3.11

##IMPORTS##
from enum import Enum
import json
import requests

##ENUM DEFINITIONS##
class requestType(Enum):
    GET = 1
    POST = 2
    PUT = 3
    PATCH = 4
    DELETE = 5

##CLASS DEFINITION##
class Api:
    ##VALUES##
    #id         Holds the ID for the API to be stored in the Database
    #reqType    Holds the type of request that the API uses 
    #data       Holds the data sent to and from the API

    ##CONSTRUCTOR##
    def __init__(self, id:str, reqType:requestType=None, data:list=[]):
        self.id = id
        self.reqType = reqType
