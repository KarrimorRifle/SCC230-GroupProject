import unittest
from server import app
import sys
from json import loads
sys.path.append((sys.path[0])[:-6])
import iota.Schedule as schedule

class test_accounts(unittest.TestCase):
    def setUp(self):
        self.client_server = app.test_client()

    def test_schedule_creation(self):
        test = iota.Schedule("Sched1","testSched",True,3,[],[],False,False)
        self.assertEqual(test['rating'], 3)

    
    # def test_accounts_get_returns_correct(self):
    #     response = self.client_server.post("/login", json={"Email": "jhondoe@gmail.com", "Password": "JhonDoe123."})
    #     self.assertEqual(response.status_code, 200)
        
    # response = self.client_server.get("/accounts")
    # self.assertEqual(loads(response.text)['AccountID'], "Accojk42VvlqdeBpOBc")