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
        test = Trigger.Trigger("Trgk09uujd33d82isjf","Schk129jd2i23kd34jf", {})

        self.assertEqual(test.id, "Trgk09uujd33d82isjf")
        self.assertEqual(test.data, {})
        self.assertEqual(test.ScheduleID, "Schk129jd2i23kd34jf")

    def test_trigger_loadFromDB(self):
        test = Trigger.loadTriggerFromDatabase("Trgk2190ej849dj345j")

        expected = Trigger.Trigger(id="Trgk2190ej849dj345j",data={'Dev4t3rgd34df423gfs':['var', '==', '4']},ScheduleID="Schk129jd2i23kd34jf")

        self.assertEqual(test.id,expected.id)
        self.assertEqual(test.ScheduleID,expected.ScheduleID)
        self.assertEqual(test.data,expected.data)
        self.assertEqual(test.debug,expected.debug)

    #add test for load from DB (requires DB creation)