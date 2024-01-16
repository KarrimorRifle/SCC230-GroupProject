import unittest
from routes.accounts import accounts
from server import app, getAccount

from flask import request, jsonify, make_response, Blueprint, current_app
import bcrypt
import uuid
from datetime import datetime, timedelta


class test_accounts(unittest.TestCase):
    def setUp(self):
        self.client_server = self.app.test_client()

    def test_server_login(self):
        response = self.client_server.post("/login")

        #checks if response status code is correct
        self.assertEqual(response.status_code, 403)

    	#checks if all error messages are correct
        exp_err_msg = "Details don't match our system"
        json_resp = response.get_json()
        self.assertEqual(json_resp.get("error"), exp_err_msg)


    #def test_account_get(self):
