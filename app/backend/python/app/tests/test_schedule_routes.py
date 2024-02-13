import unittest
from server import app

from flask import request, jsonify, make_response

class TestScheduleRoutes(unittest.TestCase):
    def setUp(self):
        self.client_server = app.test_client()
        self.client_server.post("/login", json={"Email": "jhondoe@gmail.com", "Password": "JhonDoe123."})
        self.client_server.post("/schedule", json={'Name': 'Test Schedule1'})

#     def test_create_schedule_success(self):
#         code_payload = {}
#         response = self.client_server.post('/schedule', json={'Name':'Schedule1', 'Code': code_payload})
#         self.assertEqual(response, 200)

    def test_get_schedules_success(self):
        response = self.client_server.get('/schedule')
        print(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)

#     def test_get_schedule_details_success(self):
#         response = self.client_server.get('/schedule/details', json={'ScheduleID':'1'})
#         self.assertEqual(response, 200)
#         self.assertIn('Code', response.data)
#         self.assertIn('Variables', response.data)
#         self.assertIn('Devices', response.data)
    
#     def test_delete_schedule_success(self):
#         response = self.client_server.delete('/schedule/details', json={'ScheduleID':'1'})
#         self.assertEqual(response, 200)