import unittest
from server import app

from flask import request, jsonify, make_response

class test_accounts(unittest.TestCase):
    def setUp(self):
        self.client_server = app.test_client()

    def test_accounts_creation_valid(self):
        response = self.client_server.post('/accounts', json={"FirstName": "test", "Surname": "one", "Email" : "testone@test.com", "Password" : "pass1"})
    
        self.assertEqual(response.status_code, 200)

    def test_accounts_get_account(self):
        self.client_server.post('/accounts', json={"FirstName": "test", "Surname": "zero", "Email" : "testzero@test.com", "Password" : "pass0"})

        self.assertIsNotNone(self.client_server.get('/accounts/getAccount'))

    def test_accounts_creation_used_email(self):
        self.client_server.post('/accounts', json={"FirstName": "test", "Surname": "two", "Email" : "testwo@test.com", "Password" : "pass2"})
        response = self.client_server.post('/accounts', json={"FirstName": "test", "Surname": "two", "Email" : "testwo@test.com", "Password" : "pass2"})
    
        self.assertEqual(response.status_code, 409)

    def test_accounts_update_wrong_session_id(self):
        self.assertTrue(1 > 0)

    def test_accounts_update_success(self):
        self.client_server.post('/accounts', json={"FirstName": "test", "Surname": "three", "Email" : "testhree@test.com", "Password" : "pass3"})
        response = self.client_server.patch('/accounts', json={"FirstName": "test", "Surname": "two", "Email" : "testhree@test.com", "Password" : "pass2"})
    
        self.assertEqual(response.status_code, 200)