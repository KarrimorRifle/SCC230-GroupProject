import unittest
from server import app
import sys
from json import loads
sys.path.append((sys.path[0])[:-6])
import iota.Trigger as Trigger

class test_triggers(unittest.TestCase):
    def setUp(self):
        self.client_server = app.test_client()

    def test_trigger_creation(self):
        test = Trigger.Trigger("Trig1","SchedID", {})

        self.assertEqual(test.id, "Trig1")

    def test_trigger_loadFromDB(self):
        test = Trigger.loadFromDatabase("TestTrigger")

        expected = Trigger.Trigger("TestTrigger",{'TestDevice':''},"TestSchedule")

        self.assertEqual(test,expected)

    #add test for load from DB (requires DB creation)