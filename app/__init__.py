# ~*~ encoding: utf-8 ~*~
from config import config
from flask import Flask
from flask_moment import Moment
from flask_login import LoginManager
from flask_mongokit import MongoKit

moment = Moment()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
db = MongoKit()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    moment.init_app(app)
    login_manager.init_app(app)
    db.init_app(app)

    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
