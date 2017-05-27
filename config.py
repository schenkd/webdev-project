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
        'host': os.environ['mongo_ip'] or 'localhost',
        'port': 27017
    }


class TestConfig(Config):
    # properties
    TESTING = True

    # database
    MONGODB_SETTINGS = {
        'db': 'test',
        'host': os.environ['mongo_ip'] or 'localhost',
        'port': 27017
    }


class WorkingConfig(Config):
    # database
    MONGODB_SETTINGS = {
        'db': 'lieferengpassdb',
        'host': os.environ['mongo_ip'] or 'localhost',
        'port': 27017
    }


config = {
    'dev': DevConfig,
    'test': TestConfig,
    'work': WorkingConfig,
    'default': DevConfig
}
