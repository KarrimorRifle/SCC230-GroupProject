import unittest
from server import app

from ..iota import Schedule as schedule
from json import loads

class test_accounts(unittest.TestCase):
    def setUp(self):
        self.client_server = app.test_client()

    # def test_accounts_creation_valid(self):
    #     response = self.client_server.post('/accounts', json={"FirstName": "test", "Surname": "one", "Email" : "testone@test.com", "Password" : "pass1"})
    
    #     self.assertEqual(response.status_code, 200)

    
    # def test_accounts_get_returns_correct(self):
    #     response = self.client_server.post("/login", json={"Email": "jhondoe@gmail.com", "Password": "JhonDoe123."})
    #     self.assertEqual(response.status_code, 200)
        
        response = self.client_server.get("/accounts")
        self.assertEqual(loads(response.text)['AccountID'], "Accojk42VvlqdeBpOBc")
