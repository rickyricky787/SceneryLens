import unittest
import sys
import os

from flask_app.app import app

# A single test that checks if the home page be rendered by the server.
# If they fail, something might be wrong with the Jinja syntax, the app.py file, or something else.

class testServer(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
    
    def tearDown(self):
        pass

    def test_home(self):
        with self.app as c:
            try:
                r = self.app.get("/")
            except:
                self.fail("Could not open home page.")