import unittest
from server import app
import json

class test_user(unittest.TestCase):
    def setUp(self):
        self.client_server = app.test_client()
        self.client_server.post("/login", json={"Email": "janedoe@gmail.com", "Password": "JaneDoe123."})


    def test_create_device(self):
        response = self.client_server.post("/hub/Hubk23098jwij123msd/device", json={'DeviceID': "Dev12n3kmdue9fiisnaksw3", 'DeviceName': "Test Device 1", 'Key': "12343210", 'Company': "NotTuya", 'Version': 1.0, 'IpAddress': "1.0.0.1", 'HubID': "Hubk23098jwij123msd"})
        self.assertEqual(response.status_code, 200)
        self.assertIn('DeviceID', response.data.decode('utf-8'))

    def test_delete_device(self):
        response = self.client_server.post("/hub/Hubk23098jwij123msd/device", json={'DeviceID': "Dev12n3kmdue9fiisnvdsw3", 'DeviceName': "Test Device 2", 'Key': "12343210", 'Company': "NotTuya", 'Version': 1.0, 'IpAddress': "1.0.0.2", 'HubID': "Hubk23098jwij123msd"})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        url = '/hub/Hubk23098jwij123msd/device/'
        url += data['DeviceID']
        response = self.client_server.delete(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('DeviceID', response.data.decode('utf-8'))
        
    def test_get_devices_success(self):
        response = self.client_server.post("/hub/Hubk23098jwij123msd/device", json={'DeviceID': "Dev12n3kmdue9finknaksw3", 'DeviceName': "Test Device 3", 'Key': "12343210", 'Company': "NotTuya", 'Version': 1.0, 'IpAddress': "1.0.0.3", 'HubID': "Hubk23098jwij123msd"})
        self.assertEqual(response.status_code, 200)
        response = self.client_server.get('/hub/Hubk23098jwij123msd/device')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        for entry in data:
            self.assertIn('DeviceID', entry)
            self.assertIn('DeviceName', entry)
            self.assertIn('Company', entry)
            self.assertIn('Vars', entry)

    def test_get_device_details_success(self):
        response = self.client_server.post("/hub/Hubk23098jwij123msd/device", json={'DeviceID': "Dev12n312kue9fiisnaksw3", 'DeviceName': "Test Device 4", 'Key': "12343210", 'Company': "NotTuya", 'Version': 1.0, 'IpAddress': "1.0.0.4", 'HubID': "Hubk23098jwij123msd"})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        url = '/hub/Hubk23098jwij123msd/device/'
        url += data['DeviceID']
        response = self.client_server.get(url)

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('DeviceID', data)
        self.assertIn('DeviceName', data)
        self.assertIn('Key', data)
        self.assertIn('Version', data)
        self.assertIn('IpAddress', data)
        self.assertIn('HubID', data)
        self.assertIn('Company', data)
        self.assertIn('Vars', data)
    
    def test_update_device_success(self):
        payload = {
            'DeviceName': "Test Device 5 updated",
            'Key': '000111232',
            'Version': 2.0,
        }

        response = self.client_server.post("/hub/Hubk23098jwij123msd/device", json={'DeviceID': "Dev12n3kmdue9vgvsnaksw3", 'DeviceName': "Test Device 5", 'Key': "12343210", 'Company': "NotTuya", 'Version': 1.0, 'IpAddress': "1.0.0.5", 'HubID': "Hubk23098jwij123msd"})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        url = '/hub/Hubk23098jwij123msd/device/'
        url += data['DeviceID']
        response = self.client_server.patch(url, json=payload)

        data = json.loads(response.data)
        print(data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('DeviceID', data)
        self.assertIn('DeviceName', data)
        self.assertIn('Key', data)
        self.assertIn('Version', data)
        self.assertIn('IpAddress', data)
        self.assertIn('HubID', data)
        self.assertIn('Company', data)
        self.assertIn('Vars', data)
        self.assertEqual(data['DeviceName'], payload['DeviceName'])
        self.assertEqual(data['Key'], payload['Key'])
        self.assertEqual(data['Version'], payload['Version'])
