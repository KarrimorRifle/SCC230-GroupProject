import unittest
from server import app

from flask import request, jsonify, make_response
from json import loads

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

    def test_accounts_update_success(self):
        self.client_server.post('/accounts', json={"FirstName": "test", "Surname": "nine", "Email" : "testnine@test.com", "Password" : "pass9"})
        response = self.client_server.post("/login", json={"Email": "testnine@test.com", "Password": "pass9"})
        self.assertEqual(response.status_code, 200)

        response = self.client_server.patch('/accounts', json={"Password" : "pass9", "FirstName": "test9", "Surname": "9", "Email" : "testnine2@gmail.com"})
        self.assertEqual(response.status_code, 200)

    def test_accounts_update_wrong_password(self):
        self.client_server.post('/accounts', json={"FirstName": "test", "Surname": "four", "Email" : "testfour@test.com", "Password" : "pass4"})
        response = self.client_server.post("/login", json={"Email": "testfour@test.com", "Password": "pass4"})
        self.assertEqual(response.status_code, 200)

        response = self.client_server.patch('/accounts', json={"Password" : "wrongpass", "FirstName": "test4", "Surname": "four", "Email" : "testfour2@gmail.com"})
        self.assertEqual(response.status_code, 401)

    def test_accounts_delete_success(self):
        self.client_server.post('/accounts', json={"FirstName": "test", "Surname": "five", "Email" : "testfive@test.com", "Password" : "pass5"})
        response = self.client_server.post("/login", json={"Email": "testfive@test.com", "Password": "pass5"})
        self.assertEqual(response.status_code, 200)

        response = self.client_server.delete('/accounts', json={"Password" : "pass5"})
        self.assertEqual(response.status_code, 200)

    def test_accounts_delete_wrong_password(self):
        self.client_server.post('/accounts', json={"FirstName": "test", "Surname": "six", "Email" : "testsix@test.com", "Password" : "pass6"})
        response = self.client_server.post("/login", json={"Email": "testsix@test.com", "Password": "pass6"})
        self.assertEqual(response.status_code, 200)

        response = self.client_server.delete('/accounts', json={"Password" : "wrongpass"})
        self.assertEqual(response.status_code, 401)

    def test_accounts_get_success(self):
        response = self.client_server.post("/login", json={"Email": "jhondoe@gmail.com", "Password": "JhonDoe123."})
        self.assertEqual(response.status_code, 200)
        
        response = self.client_server.get("/accounts")
        self.assertEqual(response.status_code, 200)
    
    def test_accounts_get_returns_correct(self):
        response = self.client_server.post("/login", json={"Email": "jhondoe@gmail.com", "Password": "JhonDoe123."})
        self.assertEqual(response.status_code, 200)
        
        response = self.client_server.get("/accounts")
        self.assertEqual(loads(response.text)['AccountID'], "Accojk42VvlqdeBpOBc",msg='{0}'.format(response))


class test_login_out(unittest.TestCase):
    def setUp(self):
        self.client_server = app.test_client()

    def test_login_no_data(self):
        response = self.client_server.post("/login")

        #checks if response status code is correct
        self.assertEqual(response.status_code, 415)

    def test_login_wrong_email(self):
        response = self.client_server.post("/login", json={"Email": "fake@mail.com", "Password": "JhonDoe123."})

        self.assertEqual(response.status_code, 403)

    def test_login_wrong_password(self):
        response = self.client_server.post("/login", json={"Email": "jhondoe@gmail.com", "Password": "Something"})

        self.assertEqual(response.status_code, 403)

    def test_login_correct_details(self):
        response = self.client_server.post("/login", json={"Email": "jhondoe@gmail.com", "Password": "JhonDoe123."})

        self.assertEqual(response.status_code, 200)