import unittest
import app as tested_app
import json


class FlaskAppTests(unittest.TestCase):

    def setUp(self):
        tested_app.app.config['TESTING'] = True
        self.app = tested_app.app.test_client()

    def test_get_hello_endpoint(self):
        r = self.app.get('/hellotest')
        self.assertEqual(r.data, b'Hello world!')

if __name__ == '__main__':
    unittest.main()