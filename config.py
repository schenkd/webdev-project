# ~*~ encoding: utf-8 ~*~
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # security
    WTF_CSRF_ENABLED = True
    SECRET_KEY = os.environ['SECRET_KEY'] or 'wadehaddedudenda'

    # properties
    FLASKY_POSTS_PER_PAGE = 10

    @staticmethod
    def init_app(app):
        pass


class DevConfig(Config):
    # properties
    DEBUG = True

    # database
    MONGODB_SETTINGS = {
        'db': 'dev',
        'host': os.environ['mongo_ip'],
        'port': 9999,
        'username': os.environ['mongo_user'],
        'password': os.environ['mongo_password']
    }


class TestConfig(Config):
    # properties
    TESTING = True


class WorkingConfig(Config):
    pass


config = {
    'dev': DevConfig,
    'test': TestConfig,
    'work': WorkingConfig,
    'default': DevConfig
}
