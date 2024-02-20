import unittest
from server import app
import iota.Trigger as Trigger

class test_user(unittest.TestCase):
    def setUp(self):
        self.client_server = app.test_client()

    def test_user_loadfromdatabase(self):
        pass