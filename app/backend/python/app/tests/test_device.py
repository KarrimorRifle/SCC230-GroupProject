import unittest
from server import app
import iota.Device as Device
import sys
import json
sys.path.append((sys.path[0])[:-6])

class test_user(unittest.TestCase):
    def setUp(self):
        self.client_server = app.test_client()

    def test_device_loadfromdatabase(self):
        test = Device.loadFromDatabase("Dev4t3rgd34df423gfs")

        expected = Device.Device("Dev4t3rgd34df423gfs","Test Device","Test Device","1.1.1.1","Hubk23098jwij123msd")

        self.assertEqual(test.id,expected.id)
        self.assertEqual(test.name,expected.name)
        self.assertEqual(test.deviceType,expected.deviceType)
        self.assertEqual(test.ipAddress,expected.ipAddress)
        self.assertEqual(test.hubID,expected.hubID)
        self.assertEqual(test.debug,expected.debug)

    def test_create_device(self):
        response = self.client_server.post("/device", json={'DeviceName': "Test Device", 'DeviceType':"Test", 'IpAddress':"1.1.1.2", 'HubID':"Hubk23098jwij123msd"})
        #self.assertEqual(response.status_code, 200)
        self.assertIn('DeviceID', response.data.decode('utf-8'))

    def test_delete_device(self):
        response = self.client_server.post("/device", json={'DeviceName': "Test Device 2", 'DeviceType':"Test", 'IpAddress':"1.1.1.3", 'HubID':"Hubk23098jwij123msd"})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        url = '/device/'
        url += data['DeviceID']
        response = self.client_server.delete(url)
        self.assertEqual(response.status_code, 200)
