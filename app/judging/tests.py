from app.test_base import BaseTestCase

class TestJudgingBehavior(BaseTestCase):
    def test_index_page_200(self):
        self.login()
        response = self.client.get('/judging/')
        self.assert200(response)

    def test_presentation_add_page_200(self):
        self.login()
        response = self.client.get('/judging/presentation/new')
        self.assert200(response)

    def test_technical_add_page_200(self):
        self.login()
        response = self.client.get('/judging/technical/new')
        self.assert200(response)

    def test_core_values_add_page_200(self):
        self.login()
        response = self.client.get('/judging/core_values/new')
        self.assert200(response)

