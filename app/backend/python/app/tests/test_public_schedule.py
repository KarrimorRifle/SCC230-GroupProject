import unittest
import json
from server import app

class TestPublicScheduleRoutes(unittest.TestCase):
    def setUp(self):
        self.client_server = app.test_client()
        self.client_server.post("/login", json={"Email": "janedoe@gmail.com", "Password": "JaneDoe123."})
        
        response = self.client_server.post("/hub", json={'HubName': 'Test Hub'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('HubID', data)
        self.hubID = data['HubID']

    def test_get_public_schedules(self):
        response = self.client_server.get("/schedule/public")
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

    def test_get_one_public_schedule(self):
        response = self.client_server.get('/schedule/public/Schk129jd2i23kd34af')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('ScheduleID', data)
        self.assertIn('ScheduleName', data)
        self.assertIn('Description', data)
        self.assertIn('CopyFrom', data)
        self.assertIn('IsActive', data)
        self.assertIn('IsDraft', data)
        self.assertIn('IsPublic', data)
        self.assertIn('Rating', data)
        self.assertIn('AuthorID', data)
        self.assertIn('Code', data)
        self.assertIn('VarDict', data)
        self.assertIn('Trigger', data)
        self.assertEqual(data['IsPublic'], 1)

    def test_rate_public_schedule(self):
        response = self.client_server.patch('/schedule/public/Schk129jd2i23kd34af', json={'Rating': 3})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('ScheduleID', data)
        self.assertIn('Rating', data)
        self.assertEqual(data['Rating'], 3)

        response = self.client_server.patch('/schedule/public/Schk129jd2i23kd34af', json={'Rating': 5})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('ScheduleID', data)
        self.assertIn('Rating', data)
        self.assertEqual(data['Rating'], 4)
    
    def test_rate_public_schedule_invalid_rating(self):
        response = self.client_server.patch('/schedule/public/Schk129jd2i23kd34af', json={'Rating': 6})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_save_public_schedule(self):
        response = self.client_server.post('/schedule/public/Schk129jd2i23kd34af')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)

        response = self.client_server.get('/schedule/public/Schk129jd2i23kd34af')

        self.assertEqual(response.status_code, 200)
        dataTwo = json.loads(response.data)
        
        self.assertIn('ScheduleID', data)
        self.assertIn('ScheduleName', data)
        self.assertIn('Description', data)
        self.assertIn('CopyFrom', data)
        self.assertIn('IsActive', data)
        self.assertIn('IsDraft', data)
        self.assertIn('IsPublic', data)
        self.assertIn('Rating', data)
        self.assertIn('AuthorID', data)
        self.assertIn('Code', data)
        self.assertIn('VarDict', data)
        self.assertIn('Trigger', data)
        self.assertEqual(data['ScheduleName'], dataTwo['ScheduleName'])
        self.assertEqual(data['IsPublic'], 0)
        self.assertEqual(data['AuthorID'], 'Acc89kaE64Aize3NX2j')
    
    def test_save_public_schedule_to_hub(self):
        response = self.client_server.post(f'/hub/{self.hubID}/schedule/public/Schk129jd2i23kd34af')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)

        response = self.client_server.get('/schedule/public/Schk129jd2i23kd34af')

        self.assertEqual(response.status_code, 200)
        dataTwo = json.loads(response.data)
        
        self.assertIn('ScheduleID', data)
        self.assertIn('ScheduleName', data)
        self.assertIn('Description', data)
        self.assertIn('IsActive', data)
        self.assertIn('IsDraft', data)
        self.assertIn('CopyFrom', data)
        self.assertIn('IsPublic', data)
        self.assertIn('Rating', data)
        self.assertIn('AuthorID', data)
        self.assertIn('Code', data)
        self.assertIn('VarDict', data)
        self.assertIn('Trigger', data)
        self.assertEqual(data['ScheduleName'], dataTwo['ScheduleName'])
        self.assertEqual(data['IsPublic'], 0)
        self.assertEqual(data['HubID'], self.hubID)
