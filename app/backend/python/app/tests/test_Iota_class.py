import unittest
from server import app

from flask import request, jsonify, make_response

class test_User(unittest.TestCase):
    def setUp(self):
        self.client_server = app.test_client()

    #def test_Iota(self):
        #response = self.client_server.post('/User', json={"FirstName": "test", "Surname": "one", "Email" : "testone@test.com", "Password" : "pass1"})
    
        #self.assertEqual(response.status_code, 200)
