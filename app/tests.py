from app.test_base import BaseTestCase

class TestTopLevelFunctions(BaseTestCase):
    def test_index_response(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)