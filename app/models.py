# ~*~ encoding: utf-8 ~*~
from app import db, login_manager
from datetime import datetime
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Document):
    """ Modell für den Standard-User """
    email = db.EmailField(unique=True, required=True)
    username = db.StringField(unique=True, required=True)
    password_hash = db.StringField()
    member_since = db.DateTimeField(default=datetime.utcnow)

    @staticmethod
    def generate_password(password):
        return generate_password_hash(password)

    @staticmethod
    def check_password(password_hash, password):
        return check_password_hash(password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser
