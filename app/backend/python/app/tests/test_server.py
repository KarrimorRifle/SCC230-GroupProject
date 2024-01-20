import unittest
from server import app, getAccount

from flask import request, jsonify, make_response

class test_accounts(unittest.TestCase):
    def setUp(self):
        self.client_server = app.test_client()

    def test_server_login_no_data(self):
        response = self.client_server.post("/login")

        #checks if response status code is correct
        self.assertEqual(response.status_code, 415)

    def test_server_login_wrong_email(self):
        response = self.client_server.post("/login", json={"Email": "fake@mail.com", "Password": "JhonDoe123."})

        self.assertEqual(response.status_code, 403)

    def test_server_login_wrong_password(self):
        response = self.client_server.post("/login", json={"Email": "jhondoe@gmail.com", "Password": "Something"})

        self.assertEqual(response.status_code, 403)

    def test_server_login_correct_details(self):
        response = self.client_server.post("/login", json={"Email": "jhondoe@gmail.com", "Password": "JhonDoe123."})

        self.assertEqual(response.status_code, 200)

    def test_server_get_account(self):
        self.test_server_login_correct_details()

        self.assertIsNotNone(self.client_server.get('/getAccount'))
