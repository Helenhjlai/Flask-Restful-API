import json
from restdemo.tests.base import TestBase


class TestLogin(TestBase):

    def test_login(self):
        url = '/user/{}'.format(self.username)
        res = self.client().post(
            url,
            data=json.dumps(self.user_data),
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 201)

        url = '/auth/login'
        res = self.client().post(
            url,
            data=json.dumps({'username': self.username, 'password': self.user_data['password']}),
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 200)

        res_data = json.loads(res.get_data(as_text=True))
        self.assertIn('access_token', res_data)

    def test_login_failed(self):
        url = 'user/{}'.format(self.username)
        self.client().post(
            url,
            data=json.dumps(self.user_data),
            content_type='application/json'
        )

        url = '/auth/login'
        res = self.client().post(
            url,
            data=json.dumps({'username': self.username, 'password': 'wrongpassword'}),
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 401)

        res_data = json.loads(res.get_data(as_text=True))
        message = {
            "message": "Login failed, please enter the right username or password."
        }
        self.assertEqual(res_data, message)


