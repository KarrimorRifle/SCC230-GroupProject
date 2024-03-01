import unittest
from server import app
import iota.Hub as Hub
import sys
sys.path.append((sys.path[0])[:-6])

class test_hub(unittest.TestCase):
    def setUp(self):
        self.client_server = app.test_client()

    def test_hub_loadfromdatabase(self):
        test = Hub.loadHubFromDatabase("Hubk23098jwij123msd")

        expected = Hub.Hub(id = "Hubk23098jwij123msd", name =  "Test Hub",users = { "Accojk42VvlqdeBpOBc" : 5})

        self.assertEqual(test.id,expected.id)
        self.assertEqual(test.name,expected.name)
        self.assertEqual(test.debug,expected.debug)
        self.assertEqual(test.users["Accojk42VvlqdeBpOBc"],expected.users["Accojk42VvlqdeBpOBc"])
        self.assertEqual(test.schedules,expected.schedules)