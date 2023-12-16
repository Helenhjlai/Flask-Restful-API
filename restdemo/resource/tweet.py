from flask_restful import Resource, reqparse
from restdemo.model.user import User as UserModel
from restdemo.model.tweet import Tweet as TweetModel
from flask_jwt_extended import jwt_required, get_jwt_identity


class Tweet(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'body', type=str, required=True,
        help='{body required}'
    )

    @jwt_required()
    def post(self, username):
        current_id = get_jwt_identity()
        if current_id != username:
            return {'message': 'Failed to modify.'}
        user = UserModel.get_by_username(username)
        if not user:
            return {
                'message': 'user\'s not found'
            }, 404
        data = Tweet.parser.parse_args()
        tweet = TweetModel(user_id=user.id, body=data['body'])
        tweet.add()
        return {'message': 'Add post successfully.'}

    @jwt_required()
    def get(self, username):
        user = UserModel.get_by_username(username)
        if not user:
            return {'message': 'user\'s not found'}, 404
        return [t.as_dict() for t in user.tweet]
