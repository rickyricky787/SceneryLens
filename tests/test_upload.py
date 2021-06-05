import unittest
import io
from PIL import Image
import sys
import os

from flask_app.app import app

# This set of tests checks for uploading images
class testValidation(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
    
    def tearDown(self):
        pass

    def test_jpg_upload(self):
        with self.app as c:
            with open('tests/test.jpg', 'rb') as img1:
                imgBytesIO = io.BytesIO(img1.read())

            data = {}
            data['file'] = (imgBytesIO, 'test.jpg')
            
            r = self.app.post("/", data = data, follow_redirects=True)
            if r.status_code != 200:
                self.fail("Page did not render results page.")