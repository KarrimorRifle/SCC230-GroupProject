import unittest
import json
from server import app
from flask import request

class TestHubRoutes(unittest.TestCase):
    hubID = None
    def setUp(self):
        self.client_server = app.test_client()
        self.client_server.post("/login", json={"Email": "jhondoe@gmail.com", "Password": "JhonDoe123."})

        response = self.client_server.post("/hub", json={'HubName': 'Test Hub'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('HubID', data)
        self.hubID = data['HubID']

    # def test_get_hub_schedules_success(self):
    #     response = self.client_server.get(f"/hub/{self.hubID}/schedule")
    #     self.assertEqual(response.status_code, 200)
    #     data = json.loads(response.data)
    #     self.assertIsInstance(data, list)
    #     for entry in data:
    #         self.assertIn('ScheduleID', entry)
    #         self.assertIn('ScheduleName', entry)
    #         self.assertIn('IsActive', entry)
    #         self.assertIn('Author', entry)
    #         self.assertIn('PermissionLevel', entry)
    
    # def test_get_one_hub_schedule_success(self):
    #     response = self.client_server.get(f"/hub/{self.hubID}/schedule/1")
    #     self.assertEqual(response.status_code, 200)
    #     data = json.loads(response.data)
    #     self.assertIn('ScheduleID', data)
    #     self.assertIn('ScheduleName', data)
    #     self.assertIn('IsActive', data)
    #     self.assertIn('IsPublic', data)
    #     self.assertIn('Rating', data)
    #     self.assertIn('AuthorID', data)
    #     self.assertIn('Code', data)
    #     self.assertIn('Trigger', data)