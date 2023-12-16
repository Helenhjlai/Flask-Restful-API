from restdemo import db
from werkzeug.security import generate_password_hash, check_password_hash
# from datetime import datetime, timedelta
# import jwt
# from flask import current_app
from sqlalchemy.orm import relationship
from restdemo.model.base import Base


class User(Base):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(64))

    tweet = relationship('Tweet')

    def __repr__(self):
        return "id = {}, username = {}".format(self.id, self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password=password, method='pbkdf2')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_by_username(username):
        return db.session.query(User).filter(
            User.username == username
        ).first()

    @staticmethod
    def get_by_id(user_id):
        return db.session.query(User).filter(
            User.id == user_id
        ).first()

    @staticmethod
    def get_user_list():
        return db.session.query(User).all()

    # JWT
    # def generate_token(self):
    #     """
    #     :return: generate access token
    #     """
    #     try:
    #         # set up payload with an expiration time
    #         payload = {
    #             'exp': datetime.utcnow() + timedelta(minutes=5),
    #             'iat': datetime.utcnow(),
    #             'sub': self.username
    #         }
    #         # create the byte string token using the payload and the SECRET key
    #         jwt_token = jwt.encode(
    #             payload,
    #             current_app.config.get('JWT_SECRET_KEY'),
    #             algorithm='HS256'
    #         )
    #         return jwt_token
    #     except Exception as e:
    #         return str(e)

    # flask-jwt demo
    # @staticmethod
    # def authenticate(username, password):
    #     user = db.session.query(User).filter(
    #         User.username == username
    #     ).first()
    #     if user:
    #         # check password
    #         if user.check_pasword(password):
    #             return user
    #
    # @staticmethod
    # def identity(payload):
    #     user_id = payload['identity']
    #     user = db.session.query(User).filter(
    #         User.id == user_id
    #     ).first()
    #     return user
