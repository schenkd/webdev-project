import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # security
    WTF_CSRF_ENABLED = True
    SECRET_KEY = os.getenv('SECRET_KEY') or 'wadehaddedudenda'

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
    DB_NAME = os.getenv('DB_DEV')
    DB_USER = os.getenv('DB_USER')
    DB_PW = os.getenv('DB_PW')
    SQLALCHEMY_DATABASE_URI = 'mysql://{u}:{p}@localhost/{n}'.format(u=DB_USER, p=DB_PW, n=DB_NAME)

    # properties
    DEBUG = True


class TestConfig(Config):
    # database
    # database
    DB_NAME = os.getenv('DB_TEST')
    DB_USER = os.getenv('DB_USER')
    DB_PW = os.getenv('DB_PW')
    SQLALCHEMY_DATABASE_URI = 'mysql://{u}:{p}@localhost/{n}'.format(u=DB_USER, p=DB_PW, n=DB_NAME)

    # properties
    TESTING = True


class WorkingConfig(Config):
    # database
    DB_NAME = os.getenv('DB_NAME')
    DB_USER = os.getenv('DB_USER')
    DB_PW = os.getenv('DB_PW')
    SQLALCHEMY_DATABASE_URI = 'mysql://{u}:{p}@localhost/{n}'.format(u=DB_USER, p=DB_PW, n=DB_NAME)


config = {
    'dev': DevConfig,
    'test': TestConfig,
    'work': WorkingConfig,
    'default': DevConfig
}
