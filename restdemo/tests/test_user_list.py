import json
from restdemo.tests.base import TestBase


class TestUserList(TestBase):

    def test_user_list(self):
        # create user
        url = '/user/{}'.format(self.username)
        res = self.client().post(
            url,
            data=json.dumps(self.user_data),
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 201)

        # user login
        url_login = '/auth/login'
        res = self.client().post(
            url_login,
            data=json.dumps({'username': self.username, 'password': self.user_data['password']}),
            content_type='application/json'
        )

        res_data = json.loads(res.get_data(as_text=True))
        token = res_data['access_token']

        # get user list
        url_list = '/users'
        res = self.client().get(
            url_list,
            headers={'Authorization': f'Bearer {token}'}
        )

        self.assertEqual(res.status_code, 200)
        res_list = json.loads(res.get_data(as_text=True))
        self.assertEqual(len(res_list), 1)
