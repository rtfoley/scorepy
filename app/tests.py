from app.test_base import BaseTestCase

class TestTopLevelFunctions(BaseTestCase):
    def test_index_response(self):
        response = self.client.get('/')
        self.assert200(response)
