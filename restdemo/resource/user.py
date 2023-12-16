# import jwt
from flask_restful import Resource, reqparse
# from flask import current_app

# from restdemo import db
from restdemo.model.user import User as UserModel
from flask_jwt_extended import jwt_required


def min_length_str(min_length):
    def validate(s):
        if s is None:
            raise Exception('password required')
        if not isinstance(s, (int, str)):
            raise Exception('password format error')
        s = str(s)
        if len(s) >= min_length:
            return s
        raise Exception("String must be at least %i characters long" % min_length)
    return validate


class User(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'password', type=min_length_str(5), required=True,
        help='{error_msg}'
    )
    parser.add_argument(
        'email', type=str, required=True, help='Email required.'
    )

    def get(self, username):
        """
        get user detail information
        """
        users = UserModel.get_by_username(username)
        if users:
            return users.as_dict()
        return {'message': 'user not found'}, 404

    def post(self, username):
        """ create a user"""
        users = UserModel.get_by_username(username)
        if users:
            return {'message': 'user already exist'}

        data = User.parser.parse_args()
        user_new = UserModel(
            username=username,
            email=data['email']
        )
        user_new.set_password(data['password'])

        user_new.add()
        return user_new.as_dict(), 201

    def delete(self, username):
        """delete user"""
        user_find = UserModel.get_by_username(username)

        if user_find:
            user_find.delete()
            return {'message': 'user deleted'}
        else:
            return {'message': 'user not found'}, 404

    def put(self, username):
        """update user"""
        user_find = UserModel.get_by_username(username)

        if user_find:
            data = User.parser.parse_args()
            user_find.set_password(data['password'])
            user_find.email = data['email']
            user_find.update()
            return user_find.as_dict()
        else:
            return {'message': "user not found"}, 404


class UserList(Resource):

    @jwt_required()
    def get(self):
        # token = request.headers.get('Authorization')
        # try:
        #     jwt.decode(
        #         token,
        #         current_app.config.get('JWT_SECRET_KEY'),
        #         algorithms='HS256'
        #     )
        # except jwt.ExpiredSignatureError:
        #     return {
        #         'message': 'Expired token. Please login to get an new token.'
        #     }
        # except jwt.InvalidTokenError:
        #     return {
        #         'message': 'Invalid token. Please register or login.'
        #     }
        users = UserModel.get_user_list()
        return [u.as_dict() for u in users]
