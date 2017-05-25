# ~*~ encoding: utf-8 ~*~
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # security
    WTF_CSRF_ENABLED = True
    SECRET_KEY = 'wadehaddedudenda'

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
        'host': '192.168.178.99',
        'port': 27017
    }


class TestConfig(Config):
    # properties
    TESTING = True

    # database
    MONGODB_SETTINGS = {
        'db': 'test',
        'host': '192.168.178.99',
        'port': 27017
    }


class WorkingConfig(Config):
    # database
    MONGODB_SETTINGS = {
        'db': 'lieferengpassdb',
        'host': '192.168.178.99',
        'port': 27017
    }


config = {
    'dev': DevConfig,
    'test': TestConfig,
    'work': WorkingConfig,
    'default': DevConfig
}
