import unittest
from server import app
import iota.Schedule as Schedule
import sys
sys.path.append((sys.path[0])[:-6])

class test_user(unittest.TestCase):
    def setUp(self):
        self.client_server = app.test_client()

    def test_schedule_loadfromdatabase(self):
        test = Schedule.loadFromDatabase("Schk129jd2i23kd34jf")

        expected = Schedule.Schedule(id="Schk129jd2i23kd34jf", name="Test Schedule", isPublic=False, rating=0, code=[], isActive=False, debug=False)

        self.assertEqual(test.id,expected.id)
        self.assertEqual(test.name,expected.name)
        self.assertEqual(test.isPublic,expected.isPublic)
        self.assertEqual(test.code,expected.code)
        self.assertEqual(test.isActive,expected.isActive)
        self.assertEqual(test.debug,expected.debug)