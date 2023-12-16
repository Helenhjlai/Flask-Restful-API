from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token

# from restdemo import db
from restdemo.model.user import User as UserModel


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


# flask-jwt-extended
class Login(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'password', type=min_length_str(5), required=True,
        help='{error_msg}'
    )
    parser.add_argument(
        'username', type=str, required=True, help='Username required.'
    )
    # original login without token
    # def post(self):
    #     data = Login.parser.parse_args()
    #     user = db.session.query(UserModel).filter(
    #         UserModel.username == data['username']
    #     ).first()
    #
    #     if user:
    #         if not user.check_password(data['password']):
    #             return {'message': 'Login failed, please enter the right username or password.'}
    #         return {
    #             'message': 'Login success',
    #             'token': user.generate_token()
    #         }
    #     else:
    #         return {'message': 'Login failed, please enter the right username or password.'}

    def post(self):
        data = Login.parser.parse_args()
        # username = request.json.get("username", None)
        # password = request.json.get("password", None)

        user = UserModel.get_by_username(data['username'])
        if user:
            if not user.check_password(data['password']):
                return {'message': 'Login failed, please enter the right username or password.'}, 401

        # Notice that we are passing in the actual sqlalchemy user object here
        access_token = create_access_token(identity=user.username)
        return {
            'access_token': access_token
        }
