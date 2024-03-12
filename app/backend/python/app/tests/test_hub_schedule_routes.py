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

    def test_add_hub_schedule_success(self):
        response = self.client_server.post('/schedule', json={'ScheduleName': 'Test Schedule'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        og_scheduleID = data['ScheduleID']
        url = f"/hub/{self.hubID}/schedule/{og_scheduleID}"

        response = self.client_server.post(url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('ScheduleID', data)
        self.assertIn('ScheduleName', data)
        self.assertIn('IsActive', data)
        self.assertIn('IsDraft', data)
        self.assertIn('IsPublic', data)
        self.assertIn('Rating', data)
        self.assertIn('AuthorID', data)
        self.assertIn('Code', data)
        self.assertIn('VarDict', data)
        self.assertIn('Trigger', data)
        self.assertEqual(data['HubID'], self.hubID)
        self.assertNotEqual(og_scheduleID, data['ScheduleID'])

    def test_add_hub_schedule_failure(self):
        url = f"/hub/{self.hubID}/schedule/1234567890"
        response = self.client_server.post(url)
        self.assertEqual(response.status_code, 404)

    def test_remove_hub_schedule_success(self):
        response = self.client_server.post('/schedule', json={'ScheduleName': 'Test Schedule'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        og_scheduleID = data['ScheduleID']
        url = f"/hub/{self.hubID}/schedule/{og_scheduleID}"

        response = self.client_server.post(url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('ScheduleID', data)
        self.assertIn('ScheduleName', data)
        self.assertIn('IsActive', data)
        self.assertIn('IsDraft', data)
        self.assertIn('IsPublic', data)
        self.assertIn('Rating', data)
        self.assertIn('AuthorID', data)
        self.assertIn('Code', data)
        self.assertIn('VarDict', data)
        self.assertIn('Trigger', data)
        self.assertNotEqual(og_scheduleID, data['ScheduleID'])
        self.assertEqual(data['HubID'], self.hubID)

        url = f"/hub/{self.hubID}/schedule/{data['ScheduleID']}"
        response = self.client_server.delete(url)
        self.assertEqual(response.status_code, 200)

    def test_remove_hub_schedule_failure(self):
        url = f"/hub/{self.hubID}/schedule/1234567890"
        response = self.client_server.delete(url)
        self.assertEqual(response.status_code, 403)

    def test_create_hub_schedule_success(self):
        response = self.client_server.post(f'/hub/{self.hubID}/schedule', json={'ScheduleName': 'Test Schedule'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('ScheduleID', data)
        self.assertIn('ScheduleName', data)
        self.assertIn('IsActive', data)
        self.assertIn('IsDraft', data)
        self.assertIn('IsPublic', data)
        self.assertIn('Rating', data)
        self.assertIn('AuthorID', data)
        self.assertIn('Code', data)
        self.assertIn('VarDict', data)
        self.assertIn('Trigger', data)
        self.assertEqual(data['HubID'], self.hubID)

    def test_get_hub_schedules_success(self):
        response = self.client_server.get(f"/hub/{self.hubID}/schedule")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        for entry in data:
            self.assertIn('ScheduleID', entry)
            self.assertIn('ScheduleName', entry)
            self.assertIn('IsActive', entry)
            self.assertIn('IsDraft', entry)
            self.assertIn('Author', entry)
            self.assertIn('PermissionLevel', entry)

    def test_get_hub_schedules_failure(self):
        response = self.client_server.get(f"/hub/1234567890/schedule")
        self.assertEqual(response.status_code, 401)

    def test_get_one_hub_schedule_success(self):
        response = self.client_server.post(f'/hub/{self.hubID}/schedule', json={'ScheduleName': 'Test Schedule'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        scheduleID = data['ScheduleID']

        response = self.client_server.get(f"/hub/{self.hubID}/schedule/{scheduleID}")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('ScheduleID', data)
        self.assertIn('ScheduleName', data)
        self.assertIn('IsActive', data)
        self.assertIn('IsDraft', data)
        self.assertIn('IsPublic', data)
        self.assertIn('Rating', data)
        self.assertIn('AuthorID', data)
        self.assertIn('Code', data)
        self.assertIn('VarDict', data)
        self.assertIn('Trigger', data)

    def test_get_one_hub_schedule_failure(self):
        response = self.client_server.get(f"/hub/{self.hubID}/schedule/1234567890")
        self.assertEqual(response.status_code, 403)

    def test_update_hub_schedule_success(self):
        code = [
            {
                'CommandType': 'IF',
                'Number': 1,
                'LinkedCommands': [2],
                'Params': ['5', '>=', '4'],
            },
            {
                'CommandType': 'ELSE',
                'Number': 2,
                'LinkedCommands': [],
                'Params': [],
            },
            {
                'CommandType': 'WHILE',
                'Number': 3,
                'LinkedCommands': [],
                'Params': ['9', '<=', '10'],
            }
        ]

        trigger = ['Var', '==', '5']

        newName = 'New Name Schedule'

        payload = {
            'ScheduleName': newName,
            'IsPublic': 1,
            'IsDraft': 0,
            'IsActive': 1,
            'Code': code,
            'Trigger': trigger,
        }

        response = self.client_server.post(f'/hub/{self.hubID}/schedule', json={'ScheduleName': 'Test Schedule'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        scheduleID = data['ScheduleID']
        response = self.client_server.patch(f"/hub/{self.hubID}/schedule/{scheduleID}", json=payload)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('ScheduleID', data)
        self.assertIn('ScheduleName', data)
        self.assertIn('IsActive', data)
        self.assertIn('IsDraft', data)
        self.assertIn('IsPublic', data)
        self.assertIn('Rating', data)
        self.assertIn('AuthorID', data)
        self.assertIn('Code', data)
        self.assertIn('VarDict', data)
        self.assertIn('Trigger', data)
        self.assertEqual(data['ScheduleName'], newName)
        self.assertEqual(data['IsPublic'], 1)
        self.assertEqual(data['IsDraft'], 0)
        self.assertEqual(data['IsActive'], 1)
        self.assertEqual(data['Code'], code)
        self.assertEqual(data['Trigger'], trigger)
