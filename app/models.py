# ~*~ encoding: utf-8 ~*~
from app import db, login_manager
from datetime import datetime
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash


@login_manager.user_loader
def load_user(user_id):
    return User.objects.get(id=user_id)


class User(UserMixin, db.Document):
    """ Schema für den User Document """
    email = db.EmailField(unique=True)
    password_hash = db.StringField()
    member_since = db.DateTimeField(default=datetime.utcnow)
    firstname = db.StringField()
    lastname = db.StringField()
    authorized = db.BooleanField(default=False)
    permission = db.StringField()
    last_seen = db.DateTimeField(default=datetime.utcnow)

    @staticmethod
    def generate_password(password):
        return generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def update_last_seen(self):
        self.last_seen = datetime.utcnow()
        self.save()

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Engpass(db.Document):
    """ Schema für das Engpass Document """
    pzn = db.StringField()
    atc_code = db.StringField()
    marketability = db.BooleanField(required=True)
    alternative = db.BooleanField(required=True)
    inform_expert_group = db.BooleanField(required=True)
    hospital = db.BooleanField(required=True)
    initial_report = db.DateTimeField(default=datetime.utcnow)
    other_reasons = db.StringField()
    owner = db.StringField(required=True)
    telephon = db.StringField(required=True)
    email = db.StringField(required=True)
    substance = db.StringField(required=True)
    last_report = db.DateTimeField()
    end = db.DateTimeField()
    drug_title = db.StringField()
    enr = db.IntField(required=True)
    reason = db.StringField()

    def __repr__(self):
        return '<Engpass {}>'.format(self.enr)


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser
