from datetime import timedelta
import os


class Config:
    # SQLite
    # SQLALCHEMY_DATABASE_URI = "sqlite:///demo.db"

    # MySQL
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:ltheleni_1533@localhost:3306/flask_demo'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_EXPIRATION_DELTA = timedelta(seconds=300)
    JWT_TOKEN_LOCATION = ['headers']

    # set environment variables
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'FlaskDemoAPI1533')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True


class DevelopmentConfig(Config):
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:ltheleni_1533@localhost:3306/flask_demo'
    DEBUG = True


class ProductionConfig(Config):
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:ltheleni_1533@localhost:3306/flask_prd'
    pass


app_config = {
    'testing': TestingConfig,
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
