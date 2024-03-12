import unittest
from server import app
import iota.Device as Device
import sys
sys.path.append((sys.path[0])[:-6])

class test_user(unittest.TestCase):
    def setUp(self):
        self.client_server = app.test_client()

    def test_device_loadfromdatabase(self):
        test = Device.loadDeviceFromDatabase("Dev4t3rgd34df423gfsaeft")

        expected = Device.Device(id="Dev4t3rgd34df423gfsaeft", name="Test Device", ip="192.168.0.1", key="12345678", version=1.0, company="NotTuya")

        self.assertEqual(test.id,expected.id)
        self.assertEqual(test.name,expected.name)
        self.assertEqual(test.ip,expected.ip)
        self.assertEqual(test.company,expected.company)
        if expected.company == "Tuya":
            self.assertEqual(test.version,expected.version)
            self.assertEqual(test.key,expected.key)
