import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # security
    WTF_CSRF_ENABLED = True
    SECRET_KEY = 'waddehaddedudenda'

    # database
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # properties
    FLASKY_POSTS_PER_PAGE = 10

    @staticmethod
    def init_app(app):
        pass


class DevConfig(Config):
    # database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

    # properties
    DEBUG = True


class TestConfig(Config):
    # database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')

    # properties
    TESTING = True


class WorkingConfig(Config):
    # database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'dev': DevConfig,
    'test': TestConfig,
    'work': WorkingConfig,
    'default': DevConfig
}
