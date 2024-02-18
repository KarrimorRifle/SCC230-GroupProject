import unittest
from server import app
import sys
from json import loads
sys.path.append((sys.path[0])[:-6])
import iota.Schedule as Schedule

class test_accounts(unittest.TestCase):
    def setUp(self):
        self.client_server = app.test_client()

    def test_schedule_creation_max_args(self):
        test = Schedule.Schedule("Sched1","testSched",True,3,[],False,False)

        self.assertEqual(test.rating, 3)

    def test_schedule_creation_min_args(self):
        test = Schedule.Schedule("Sched1","testSched")

        self.assertEqual(test.name, "testSched")