from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

# from flask_jwt import JWT

db = SQLAlchemy()
migrate = Migrate()

from restdemo.resource.hello import HelloWorld
from restdemo.resource.user import User, UserList
from restdemo.resource.tweet import Tweet
from restdemo.resource.auth import Login
from restdemo.config import app_config

jwt = JWTManager()


def create_app(config_name='development'):
    app = Flask(__name__)
    api = Api(app)
    app.config.from_object(app_config[config_name])
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    api.add_resource(HelloWorld, '/')
    api.add_resource(User, '/user/<string:username>')
    api.add_resource(UserList, '/users')
    api.add_resource(Login, '/auth/login')
    api.add_resource(Tweet, '/tweet/<string:username>')

    return app
