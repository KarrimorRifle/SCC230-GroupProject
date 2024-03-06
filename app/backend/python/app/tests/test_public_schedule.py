import unittest
import json
from server import app

class TestPublicScheduleRoutes(unittest.TestCase):
    def setUp(self):
        self.client_server = app.test_client()
        self.client_server.post("/login", json={"Email": "jhondoe@gmail.com", "Password": "JhonDoe123."})

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
        self.assertIn('IsActive', data)
        self.assertIn('IsDraft', data)
        self.assertIn('IsPublic', data)
        self.assertIn('Rating', data)
        self.assertIn('AuthorID', data)
        self.assertIn('Code', data)
        self.assertIn('Trigger', data)