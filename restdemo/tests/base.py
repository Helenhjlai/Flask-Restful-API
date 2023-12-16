import unittest
from restdemo import create_app, db


class TestBase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client
        self.username = 'testing1'
        self.user_data = {
            'password': 'testing1_12345',
            'email': 'testing1@trendmirco.com'
        }
        self.data_update = {
            'password': 'newpassword',
            'email': 'newemail@trendmirco.com'
        }
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
