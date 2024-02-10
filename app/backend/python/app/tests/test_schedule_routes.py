import unittest
from server import app

from flask import request, jsonify, make_response

class TestScheduleRoutes(unittest.TestCase):
    def setUp(self):
        self.client_server = app.test_client()
        self.client_server.post("/login", json={"Email": "jhondoe@gmail.com", "Password": "JhonDoe123."})

    def test_create_schedule_success(self):
        response = self.client_server.post('/schedule', json={'Name':'Schedule1', 'Code': ''})
        self.assertEqual(response, 200)

