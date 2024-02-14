import unittest
import json
from server import app

from flask import request, jsonify, make_response

class TestScheduleRoutes(unittest.TestCase):
    def setUp(self):
        self.client_server = app.test_client()
        self.client_server.post("/login", json={"Email": "jhondoe@gmail.com", "Password": "JhonDoe123."})

    def test_create_schedule_success(self):
        response = self.client_server.post("/schedule", json={'ScheduleName': 'Test Schedule1', 'IsActive': 0, 'IsPublic': 0, 'Rating': 0})
        self.assertEqual(response.status_code, 200)
        self.assertIn('EventID', response.data.decode('utf-8'))

    def test_delete_schedule_success(self):
        response = self.client_server.post("/schedule", json={'ScheduleName': 'Test Schedule2', 'IsActive': 0, 'IsPublic': 0, 'Rating': 0})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        url = '/schedule/'
        url += str(data['EventID'])
        response = self.client_server.delete(url)
        self.assertEqual(response.status_code, 200)

    def test_get_schedules_success(self):
        response = self.client_server.post("/schedule", json={'ScheduleName': 'Test Schedule2', 'IsActive': 0, 'IsPublic': 0, 'Rating': 0})
        self.assertEqual(response.status_code, 200)
        response = self.client_server.get('/schedule')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        for entry in data:
            self.assertIn('EventID', entry)
            self.assertIn('ScheduleName', entry)
            self.assertIn('IsActive', entry)
            self.assertIn('IsPublic', entry)
            self.assertIn('Rating', entry)

    # def test_get_schedule_details_success(self):
    #     response = self.client_server.get('/schedule/1')
    #     print(response.data.decode('utf-8'))
    #     self.assertEqual(response.status_code, 200)