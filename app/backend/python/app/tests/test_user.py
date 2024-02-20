import unittest
from server import app
import iota.User as User

class test_user(unittest.TestCase):
    def setUp(self):
        self.client_server = app.test_client()

    def test_user_loadfromdatabase(self):
        test = User.loadFromDatabase("TestTrigger")

        expected = User.User("TestTrigger",{'TestDevice':''},"TestSchedule")

        self.assertEqual(test,expected)