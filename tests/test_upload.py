import unittest
import io
from PIL import Image
import sys
import os

from flask_app.app import app

# This set of tests checks for uploading images
class testUpload(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
    
    def tearDown(self):
        pass

    def test_jpg_upload(self):
        with self.app as c:
            with open('tests/test.jpg', 'rb') as img1:
                imgBytesIO = io.BytesIO(img1.read())

            data = {'img_link': ""}
            data['file'] = (imgBytesIO, 'test.jpg')
            
            r = self.app.post("/", data = data, follow_redirects=True)
            if r.status_code != 200:
                self.fail("Page did not render results page.")
    
    def test_img_url(self):
        with self.app as c:
            data = {
                "img_link": "https://picsum.photos/id/1043/5184/3456",
                "file": ""
            }      

            r = self.app.post("/", data = data, follow_redirects=True)
            if r.status_code != 200:
                self.fail("Page did not render results page.")