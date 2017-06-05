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

    meta = {
        'indexes': [
            'email',
            'authorized'
        ]
    }

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


class Drug(db.Document):
    """ Schema für das Arzneimittel Document """
    enr = db.IntField()
    atc_code = db.StringField()
    drug_title = db.StringField()
    hospital = db.BooleanField()
    marketability = db.BooleanField()
    substance = db.ListField(db.StringField)

    meta = {
        'indexes': [
            'enr',
            'substance'
        ]
    }

    def __repr__(self):
        return '<Drug {}>'.format(self.enr)


class Producer(db.Document):
    """ Schema für das Hersteller Document """
    name = db.StringField()
    pnr = db.IntField()
    employee = db.ListField(db.ReferenceField(User))

    meta = {
        'indexes': [
            'pnr'
        ]
    }

    def attach_random_user(self):
        User.objects.get()

    def __repr__(self):
        return '<Producer {}>'.format(self.name)


class Engpass(db.Document):
    """ Schema für das Engpass Document """
    # string
    other_reasons = db.StringField()
    telephone = db.StringField()
    email = db.StringField()
    reason = db.StringField()

    # bools
    alternative = db.BooleanField()
    inform_expert_group = db.BooleanField()

    # datetime
    initial_report = db.DateTimeField(default=datetime.utcnow)
    last_report = db.DateTimeField(default=datetime.utcnow)
    end = db.DateTimeField()

    # int
    pzn = db.IntField()

    # ref
    drug = db.ReferenceField(Drug)
    producer = db.ReferenceField(Producer)

    meta = {
        'indexes': [
            'producer'
        ]
    }

    def update_last_report(self):
        self.last_report = datetime.utcnow()
        self.save()

    def __repr__(self):
        return '<Engpass {}>'.format(self.enr)


class AnonymousUser(AnonymousUserMixin):
    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser
