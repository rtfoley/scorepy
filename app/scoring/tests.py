from app.test_base import BaseTestCase

class TestScoringBehavior(BaseTestCase):
    def test_index_page_200(self):
        self.login()
        response = self.client.get('/scores/')
        self.assert200(response)

    def test_add_page_200(self):
        self.login()
        response = self.client.get('/scores/add')
        self.assert200(response)