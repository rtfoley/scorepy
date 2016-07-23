import unittest
from app import create_app

class TestScorepy(unittest.TestCase):
    def setUp(self):
        app = create_app('config.TestingConfiguration')
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_index_response(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
