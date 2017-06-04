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
    firstname = db.StringField()
    lastname = db.StringField()
    permission = db.StringField()
    authorized = db.BooleanField(default=False)
    member_since = db.DateTimeField(default=datetime.utcnow)
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
    # string
    pzn = db.StringField()
    atc_code = db.StringField()
    other_reasons = db.StringField()
    owner = db.StringField()
    telephone = db.StringField()
    email = db.StringField()
    substance = db.StringField()
    drug_title = db.StringField()
    reason = db.StringField()

    # bools
    marketability = db.BooleanField()
    alternative = db.BooleanField()
    inform_expert_group = db.BooleanField()
    hospital = db.BooleanField()

    # datetime
    initial_report = db.DateTimeField(default=datetime.utcnow)
    last_report = db.DateTimeField(default=datetime.utcnow)
    end = db.DateTimeField()

    # int
    enr = db.IntField()

    def update_last_report(self):
        self.last_report = datetime.utcnow()
        self.save()

    def __repr__(self):
        return '<Engpass {}>'.format(self.enr)


class AnonymousUser(AnonymousUserMixin):
    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser
