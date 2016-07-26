from app.test_base import BaseTestCase

class TestTeamBehavior(BaseTestCase):
    def test_index_page_200(self):
        self.login()
        response = self.client.get('/teams/')
        self.assert200(response)

    def test_add_page_200(self):
        self.login()
        response = self.client.get('/teams/new')
        self.assert200(response)