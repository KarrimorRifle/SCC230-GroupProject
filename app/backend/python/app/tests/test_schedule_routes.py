import unittest
import json
from server import app

class TestScheduleRoutes(unittest.TestCase):
    def setUp(self):
        self.client_server = app.test_client()
        self.client_server.post("/login", json={"Email": "jhondoe@gmail.com", "Password": "JhonDoe123."})

    def test_create_schedule_success(self):
        response = self.client_server.post("/schedule", json={'ScheduleName': 'Test Schedule1'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('ScheduleID', response.data.decode('utf-8'))

    def test_delete_schedule_success(self):
        response = self.client_server.post("/schedule", json={'ScheduleName': 'Test Schedule2'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        url = '/schedule/'
        url += data['ScheduleID']

        response = self.client_server.delete(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(data['ScheduleID'], response.data.decode('utf-8'))

    def test_get_schedules_success(self):
        response = self.client_server.post("/schedule", json={'ScheduleName': 'Test Schedule2'})
        self.assertEqual(response.status_code, 200)
        response = self.client_server.get('/schedule')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        
        for entry in data:
            self.assertIn('ScheduleID', entry)
            self.assertIn('ScheduleName', entry)
            self.assertIn('IsActive', entry)
            self.assertIn('IsDraft', entry)
            self.assertIn('IsPublic', entry)
            self.assertIn('Rating', entry)

    def test_get_schedule_details_success(self):
        response = self.client_server.post("/schedule", json={'ScheduleName': 'Test Schedule2'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        url = '/schedule/'
        url += data['ScheduleID']
        response = self.client_server.get(url)

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('ScheduleID', data)
        self.assertIn('ScheduleName', data)
        self.assertIn('IsActive', data)
        self.assertIn('IsDraft', data)
        self.assertIn('IsPublic', data)
        self.assertIn('Rating', data)
        self.assertIn('AuthorID', data)
        self.assertIn('Code', data)
        self.assertIn('Trigger', data)
    
    def test_update_schedule_success(self):
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

        val1 = ['Var', '==', '5']
        val2 = ['Var2', '==', '8']
        trigger = {'Dev4t3rgd34df423gfs': val1, 'Dev4t3rgd34df423gfs': val2}

        newName = 'Name Update Schedule3'

        payload = {
            'ScheduleName': newName,
            'IsPublic': 1,
            'IsDraft': 0,
            'IsActive': 1,
            'Code': code,
            'Trigger': trigger,
        }

        response = self.client_server.post("/schedule", json={'ScheduleName': 'Test Schedule3'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        url = '/schedule/'
        id = data['ScheduleID']
        url += id
        response = self.client_server.patch(url, json=payload)

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('ScheduleID', data)
        self.assertIn('ScheduleName', data)
        self.assertIn('IsActive', data)
        self.assertIn('IsDraft', data)
        self.assertIn('IsPublic', data)
        self.assertIn('Rating', data)
        self.assertIn('AuthorID', data)
        self.assertIn('Code', data)
        self.assertIn('Trigger', data)
        self.assertEqual(data['ScheduleName'], newName)
        self.assertEqual(data['IsPublic'], 1)
        self.assertIn(code[0], data['Code'])
        self.assertIn(code[1], data['Code'])
        self.assertIn(code[2], data['Code'])

    def test_update_schedule_failure(self):
        payload = {
            'IsDraft': 1,
            'IsActive': 1,
        }

        response = self.client_server.post("/schedule", json={'ScheduleName': 'Test Schedule3'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        url = '/schedule/'
        id = data['ScheduleID']
        url += id
        response = self.client_server.patch(url, json=payload)

        self.assertEqual(response.status_code, 400)