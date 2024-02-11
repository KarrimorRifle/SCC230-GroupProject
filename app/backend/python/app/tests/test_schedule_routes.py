# import unittest
# from server import app

# from flask import request, jsonify, make_response

# class TestScheduleRoutes(unittest.TestCase):
#     def setUp(self):
#         self.client_server = app.test_client()
#         self.client_server.post("/login", json={"Email": "jhondoe@gmail.com", "Password": "JhonDoe123."})

#     def test_create_schedule_success(self):
#         code_payload = {}
#         response = self.client_server.post('/schedule', json={'Name':'Schedule1', 'Code': code_payload})
#         self.assertEqual(response, 200)

#     def test_get_schedules_success(self):
#         response = self.client_server.get('/schedule')
#         self.assertEqual(response, 200)
#         self.assertIn('EventID', response.data)
#         self.assertIn('Name', response.data)
#         self.assertIn('IsActive', response.data)
#         self.assertIn('IsPublic', response.data)
#         self.assertIn('Rating', response.data)

#     def test_get_schedule_details_success(self):
#         response = self.client_server.get('/schedule/details', json={'ScheduleID':'1'})
#         self.assertEqual(response, 200)
#         self.assertIn('Code', response.data)
#         self.assertIn('Variables', response.data)
#         self.assertIn('Devices', response.data)
    
#     def test_delete_schedule_success(self):
#         response = self.client_server.delete('/schedule/details', json={'ScheduleID':'1'})
#         self.assertEqual(response, 200)