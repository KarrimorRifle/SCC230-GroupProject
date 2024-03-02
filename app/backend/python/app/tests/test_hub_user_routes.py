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
    
    def test_get_hub_users_success(self):
        response = self.client_server.get(f"/hub/{self.hubID}/user")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        for entry in data:
            self.assertIn('AccountID', entry)
            self.assertIn('PermissionLevel', entry)

    def test_get_one_hub_user_success(self):
        response = self.client_server.get(f"/hub/{self.hubID}/user/Accojk42VvlqdeBpOBc")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('AccountID', data)
        self.assertIn('PermissionLevel', data)

    def test_get_one_hub_user_failure(self):
        response = self.client_server.get(f"/hub/{self.hubID}/user/0")
        self.assertEqual(response.status_code, 404)

    def test_force_add_to_hub_success(self):
        response = self.client_server.post(f"/hub/{self.hubID}/user", json={'AccountID': 'Acc89kaE64Aize3NX2j', 'PermissionLevel': 3})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('AccountID', data)
        self.assertIn('PermissionLevel', data)

        response = self.client_server.delete(f"/hub/{self.hubID}/user/{data['AccountID']}")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('AccountID', data)
        self.assertIn('HubID', data)

    def test_manage_hub_user_success(self):
        response = self.client_server.post(f"/hub/{self.hubID}/user", json={'AccountID': 'Acc89kaE64Aize3NX2j', 'PermissionLevel': 3})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('AccountID', data)
        self.assertIn('PermissionLevel', data)

        response = self.client_server.patch(f"/hub/{self.hubID}/user/Acc89kaE64Aize3NX2j", json={'PermissionLevel': 2})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('AccountID', data)
        self.assertIn('PermissionLevel', data)

    def test_manage_hub_user_failure(self):
        response = self.client_server.patch(f"/hub/{self.hubID}/user/0", json={'PermissionLevel': 4})
        self.assertEqual(response.status_code, 404)

    def test_remove_hub_user_success(self):
        response = self.client_server.post(f"/hub/{self.hubID}/user", json={'AccountID': 'Acc89kaE64Aize3NX2j', 'PermissionLevel': 3})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('AccountID', data)
        self.assertIn('PermissionLevel', data)

        response = self.client_server.delete(f"/hub/{self.hubID}/user/{data['AccountID']}")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('AccountID', data)
        self.assertIn('HubID', data)

    def test_create_invite_token_success(self):
        response = self.client_server.post(f"/hub/{self.hubID}/invite")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('Token', data)

    def test_join_hub_success(self):
        response = self.client_server.post(f"/hub/invite/testToken")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('HubID', data)

    def test_join_hub_failure(self):
        response = self.client_server.post(f"/hub/invite/0")
        self.assertEqual(response.status_code, 404)
    
    def test_leave_hub_success(self):
        response = self.client_server.delete(f"/hub/{self.hubID}/user")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('HubID', data)
    