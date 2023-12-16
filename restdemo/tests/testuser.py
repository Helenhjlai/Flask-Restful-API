import json
from werkzeug.security import check_password_hash

from restdemo.tests.base import TestBase


class TestUser(TestBase):

    def test_user_create(self):
        url = '/user/{}'.format(self.username)
        res = self.client().post(
            url,
            data=json.dumps(self.user_data),
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 201)

        res_data = json.loads(res.get_data(as_text=True))
        self.assertEqual(res_data.get('username'), self.username)
        self.assertEqual(res_data.get('email'), self.user_data['email'])

        res = self.client().post(
            url,
            data=json.dumps(self.user_data),
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 200)

        res_data = json.loads(res.get_data(as_text=True))
        self.assertEqual(res_data.get('message'), 'user already exist')

    def test_user_get(self):
        url = '/user/{}'.format(self.username)
        self.client().post(
            url,
            data=json.dumps(self.user_data),
            content_type='application/json'
        )

        res = self.client().get(url)
        self.assertEqual(res.status_code, 200)

        res_data = json.loads(res.get_data(as_text=True))
        self.assertEqual(res_data.get('username'), self.username)
        self.assertEqual(res_data.get('email'), self.user_data['email'])

    def test_user_get_not_exist(self):
        url = '/user/{}'.format(self.username)
        res = self.client().get(url)
        res_data = json.loads(res.get_data(as_text=True))

        self.assertEqual(res.status_code, 404)
        self.assertEqual(res_data, {'message': 'user not found'})

    def test_user_delete(self):
        url = 'user/{}'.format(self.username)
        self.client().post(
            url,
            data=json.dumps(self.user_data),
            content_type='application/json'
        )

        res = self.client().delete(url)
        self.assertEqual(res.status_code, 200)

        res_data = json.loads(res.get_data(as_text=True))
        self.assertEqual(res_data, {'message': 'user deleted'})

    def test_user_delete_not_exist(self):
        url = 'user/{}'.format(self.username)
        res = self.client().delete(url)

        self.assertEqual(res.status_code, 404)
        res_data = json.loads(res.get_data(as_text=True))
        self.assertEqual(res_data, {'message': 'user not found'})

    def test_user_update(self):
        url = 'user/{}'.format(self.username)
        res = self.client().post(
            url,
            data=json.dumps(self.user_data),
            content_type='application/json'
        )

        res = self.client().put(
            url,
            data=json.dumps(self.data_update),
            content_type='application/json'
        )

        self.assertEqual(res.status_code, 200)
        res_data = json.loads(res.get_data(as_text=True))
        self.assertEqual(check_password_hash(res_data.get('password_hash'), self.data_update['password']), True)

    def test_user_update_not_exist(self):
        url = 'user/{}'.format(self.username)
        data_update = {
            'password': 'newpassword',
            'email': 'testing1@trendmirco.com'
        }

        res = self.client().put(
            url,
            data=json.dumps(data_update),
            content_type='application/json'
        )

        self.assertEqual(res.status_code, 404)
        res_data = json.loads(res.get_data(as_text=True))
        self.assertEqual(res_data, {'message': 'user not found'})
