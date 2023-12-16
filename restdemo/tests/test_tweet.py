import json
from restdemo.tests.base import TestBase


class TestLogin(TestBase):

    def test_tweet_post(self):
        # create user
        url = '/user/{}'.format(self.username)
        res = self.client().post(
            url,
            data=json.dumps(self.user_data),
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 201)

        # user login to get token
        url = '/auth/login'
        res = self.client().post(
            url,
            data=json.dumps({'username': self.username, 'password': self.user_data['password']}),
            content_type='application/json'
        )
        res_data = json.loads(res.get_data(as_text=True))
        token = res_data['access_token']
        access_token = f'Bearer {token}'

        # tweet post
        url = '/tweet/{}'.format(self.username)
        res = self.client().post(
            url,
            data=json.dumps({'body': 'testtesttest'}),
            content_type='application/json',
            headers={'Authorization': access_token}
        )

        self.assertEqual(res.status_code, 200)
        res_data = json.loads(res.get_data(as_text=True))
        message = {
            'message': 'Add post successfully.'
        }
        self.assertEqual(res_data, message)

    def test_tweet_get(self):
        # create user
        url = '/user/{}'.format(self.username)
        res = self.client().post(
            url,
            data=json.dumps(self.user_data),
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 201)

        # user login to get token
        url = '/auth/login'
        res = self.client().post(
            url,
            data=json.dumps({'username': self.username, 'password': self.user_data['password']}),
            content_type='application/json'
        )
        res_data = json.loads(res.get_data(as_text=True))
        token = res_data['access_token']
        access_token = f'Bearer {token}'

        # tweet post
        url = '/tweet/{}'.format(self.username)
        body = 'testtesttest'
        res = self.client().post(
            url,
            data=json.dumps({'body': body}),
            content_type='application/json',
            headers={'Authorization': access_token}
        )

        # tweet post get
        url = '/tweet/{}'.format(self.username)
        res = self.client().get(
            url,
            headers={'Authorization': access_token}
        )

        self.assertEqual(res.status_code, 200)
        res_data = json.loads(res.get_data(as_text=True))

        self.assertEqual(len(res_data), 1)
