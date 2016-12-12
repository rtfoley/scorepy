from app.test_base import BaseTestCase


class TestTopLevelFunctions(BaseTestCase):
    def test_index_response(self):
        response = self.client.get('/')
        self.assert200(response)

    def test_login_required(self):
        self.check_login_required('/scores/add', '/login?next=%2Fscores%2Fadd')
        self.check_login_required('/settings', '/login?next=%2Fsettings')
        self.check_login_required('/review', '/login?next=%2Freview')
        self.check_login_required('/teams/new', '/login?next=%2Fteams%2Fnew')
        self.check_login_required('/scores/playoffs', '/login?next=%2Fscores%2Fplayoffs')

    def check_login_required(self, attempted_location, redirected_location):
        response = self.client.get(attempted_location)
        self.assertTrue(response.status_code in (301, 302))
        self.assertEqual(response.location, 'http://localhost' + redirected_location)
        self.login('admin', 'changeme')
        response = self.client.get(attempted_location)
        self.assert200(response)
        self.logout()
