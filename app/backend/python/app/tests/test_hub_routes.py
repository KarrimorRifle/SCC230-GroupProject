import unittest
import json
from server import app

class TestHubRoutes(unittest.TestCase):
    def setUp(self):
        self.client_server = app.test_client()
        self.client_server.post("/login", json={"Email": "jhondoe@gmail.com", "Password": "JhonDoe123."})

    def test_create_hub_success(self):
        response = self.client_server.post("/hub", json={'HubName': 'Test Hub1'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('HubID', response.data.decode('utf-8'))

    def test_delete_hub_success(self):
        response = self.client_server.post("/hub", json={'HubName': 'Test Hub2'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        url = '/hub/'
        url += data['HubID']

        response = self.client_server.delete(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(data['HubID'], response.data.decode('utf-8'))

    def test_get_hubs_success(self):
        response = self.client_server.post("/hub", json={'HubName': 'Test Hub'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('HubID', response.data.decode('utf-8'))

        response = self.client_server.get("/hub")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)

        self.assertIsInstance(data, list)
        for entry in data:
            self.assertIn('HubID', entry)
            self.assertIn('HubName', entry)
    
    def test_get_one_hub_success(self):
        response = self.client_server.post("/hub", json={'HubName': 'Test Hub3'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        url = '/hub/'
        url += data['HubID']
        response = self.client_server.get(url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)

        self.assertIn('HubID', data)
        self.assertIn('HubName', data)
        self.assertEqual(data['HubName'], 'Test Hub3')

    def test_update_hub_success(self):
        response = self.client_server.post("/hub", json={'HubName': 'Test Hub1'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        url = '/hub/'
        url += data['HubID']
        response = self.client_server.patch(url, json={'HubName': 'Test Hub2'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)

        self.assertIn('HubID', data)
        self.assertIn('HubName', data)
        self.assertEqual(data['HubName'], 'Test Hub2')