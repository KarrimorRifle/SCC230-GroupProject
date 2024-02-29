import unittest
from server import app
import iota.User as User
import sys
sys.path.append((sys.path[0])[:-6])

class test_user(unittest.TestCase):
    def setUp(self):
        self.client_server = app.test_client()

    def test_user_loadfromdatabase(self):
        test = User.loadUserFromDatabase("Accojk42VvlqdeBpOBc")

        expected = User.User("Accojk42VvlqdeBpOBc", "Jhon", None, "jhondoe@gmail.com")

        self.assertEqual(test.id,expected.id)
        self.assertEqual(test.username,expected.username)
        self.assertEqual(test.password,expected.password)
        self.assertEqual(test.email,expected.email)
        self.assertEqual(test.allowEmails,expected.allowEmails)
        self.assertEqual(test.debug,expected.debug)