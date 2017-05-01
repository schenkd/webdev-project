# ~*~ encoding: utf-8 ~*~
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # security
    WTF_CSRF_ENABLED = True
    SECRET_KEY = os.getenv('SECRET_KEY') or 'wadehaddedudenda'

    # properties
    FLASKY_POSTS_PER_PAGE = 10

    @staticmethod
    def init_app(app):
        pass


class DevConfig(Config):
    # database
    MONGODB_SETTINGS = {
        'db': 'app',
        'host': 'localhost',
        'port': 27017
    }

    # properties
    DEBUG = True


class TestConfig(Config):
    # database
    MONGODB_SETTINGS = {
        'db': 'app',
        'host': 'localhost',
        'port': 27017
    }

    # properties
    TESTING = True


class WorkingConfig(Config):
    # database
    MONGODB_SETTINGS = {
        'db': 'app',
        'host': 'localhost',
        'port': 27017,
        'username': '',
        'password': ''
    }


config = {
    'dev': DevConfig,
    'test': TestConfig,
    'work': WorkingConfig,
    'default': DevConfig
}
