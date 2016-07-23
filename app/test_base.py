from flask.ext.testing import TestCase
import unittest
from app import create_app, db

class BaseTestCase(TestCase):
    def create_app(self):
        return create_app('config.TestingConfiguration')

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def login(self, username, password):
        return self.client.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.client.get('/logout', follow_redirects=True)

if __name__ == '__main__':
    unittest.main()
