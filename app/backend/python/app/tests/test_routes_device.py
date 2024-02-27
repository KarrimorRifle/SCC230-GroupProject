import unittest
from server import app
import json

class test_user(unittest.TestCase):
    def setUp(self):
        self.client_server = app.test_client()
        self.client_server.post("/login", json={"Email": "jhondoe@gmail.com", "Password": "JhonDoe123."})


    def test_create_device(self):
        response = self.client_server.post("/device", json={'DeviceName': "Test Device 2", 'DeviceType':"Test", 'IpAddress':"1.1.1.2", 'HubID':"Hubk23098jwij123msd"})
        #self.assertEqual(response.status_code, 200)
        self.assertIn('DeviceID', response.data.decode('utf-8'))

    def test_delete_device(self):
        response = self.client_server.post("/device", json={'DeviceName': "Test Device 3", 'DeviceType':"Test", 'IpAddress':"1.1.1.3", 'HubID':"Hubk23098jwij123msd"})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        url = '/device/'
        url += data['DeviceID']
        response = self.client_server.delete(url)
        self.assertEqual(response.status_code, 200)
        
    def test_get_devices_success(self):
        response = self.client_server.post("/device", json={'DeviceName': "Test Device 3", 'DeviceType':"Test", 'IpAddress':"1.1.1.3", 'HubID':"Hubk23098jwij123msd"})
        self.assertEqual(response.status_code, 200)
        response = self.client_server.get('/device', json={'HubID':"Hubk23098jwij123msd"})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        for entry in data:
            self.assertIn('DeviceID', entry)
            self.assertIn('DeviceName', entry)
            self.assertIn('DeviceType', entry)

    def test_get_device_details_success(self):
        response = self.client_server.post("/device", json={'DeviceName': "Test Device 4", 'DeviceType':"Test", 'IpAddress':"1.1.1.4", 'HubID':"Hubk23098jwij123msd"})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        url = '/device/'
        url += data['DeviceID']
        response = self.client_server.get(url)

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('DeviceID', data)
        self.assertIn('DeviceName', data)
        self.assertIn('DeviceType', data)
        self.assertIn('IpAddress', data)
        self.assertIn('HubID', data)
    
    def test_update_schedule_success(self):
        payload = {
            'DeviceName': "Test Device 5 updated",
        }

        response = self.client_server.post("/device", json={'DeviceName': "Test Device 5", 'DeviceType':"Test", 'IpAddress':"1.1.1.5", 'HubID':"Hubk23098jwij123msd"})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        url = '/device/'
        id = data['DeviceID']
        url += id
        response = self.client_server.patch(url, json=payload)

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('DeviceID', data)
        self.assertIn('DeviceName', data)
        self.assertIn('DeviceType', data)
        self.assertIn('IpAddress', data)
        self.assertIn('HubID', data)
        self.assertEqual(data['DeviceName'], payload['DeviceName'])
