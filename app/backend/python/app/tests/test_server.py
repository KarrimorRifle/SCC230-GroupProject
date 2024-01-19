import unittest
from unittest.mock import patch, MagicMock
from routes.accounts import accounts
from server import app, getAccount

from flask import request, jsonify, make_response, Blueprint, current_app
import bcrypt
import uuid
from datetime import datetime, timedelta

class test_accounts(unittest.TestCase):
    def setUp(self):
        self.client_server = app.test_client()

    def test_server_login_no_data(self):
        response = self.client_server.post("/login")

        #checks if response status code is correct
        self.assertEqual(response.status_code, 415)

    def test_server_login_wrong_email(self):
        response = self.client_server.post("/login", json={"Email": "fake@mail.com", "Password": "fakePassword"})

        self.assertEqual(response.status_code, 403)

    def test_server_login_correct_details(self):
        response = self.client_server.post("/login", json={"Email": "jhondoe@gmail.com", "Password": "JhonDoe123."})

        self.assertEqual(response.status_code, 200)
