# ~*~ encoding: utf-8 ~*~
from app import db, login_manager
from datetime import datetime
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash


@login_manager.user_loader
def load_user(user_id):
    return User.objects.get(id=user_id)


class User(UserMixin, db.DynamicDocument):
    """ Schema für den User Document """
    # string
    password_hash = db.StringField()
    firstname = db.StringField()
    lastname = db.StringField()
    permission = db.StringField()
    email = db.EmailField(unique=True)

    # bool
    authorized = db.BooleanField(default=False)

    # datetime
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
        return '<User {}>'.format(self.email)


class Drug(db.Document):
    """ Schema für das Arzneimittel Document """
    # int
    enr = db.IntField()
    pzn = db.IntField()

    # string
    atc_code = db.StringField()
    drug_title = db.StringField()

    # bool
    hospital = db.BooleanField()
    marketability = db.BooleanField()

    # list
    substance = db.ListField(db.StringField())

    meta = {
        'indexes': [
            'enr',
            'substance'
        ]
    }

    @staticmethod
    def get_by_enr(enr):
        return Drug.objects.get(enr=enr)

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

    @staticmethod
    def get_by_employee(email):
        return Producer.objects.get(employee=User.objects.get(email=email))

    def __repr__(self):
        return '<Producer {}>'.format(self.name)


class Engpass(db.Document):
    """ Schema für das Engpass Document """
    # string
    other_reasons = db.StringField()
    telephone = db.StringField()
    email = db.StringField()
    reason = db.StringField()

    # bool
    alternative = db.BooleanField()
    inform_expert_group = db.BooleanField()

    # datetime
    initial_report = db.DateTimeField(default=datetime.utcnow)
    last_report = db.DateTimeField(default=datetime.utcnow)
    end = db.DateTimeField()

    # ref
    drug = db.ReferenceField(Drug)
    producer = db.ReferenceField(Producer)

    meta = {
        'indexes': [
            'producer'
        ]
    }

    @staticmethod
    def get_by_enr(enr):
        return Engpass.objects.get(drug=Drug.objects.get(enr=enr))

    def update_last_report(self):
        self.last_report = datetime.utcnow()
        self.save()

    def __repr__(self):
        return '<Engpass {}>'.format(self.enr)


class Contact(db.Document):
    """ Schema für das Kontakt Document """
    firstname = db.StringField()
    lastname = db.StringField()
    message = db.StringField()
    telephone = db.StringField()
    email = db.EmailField()
    timestamp = db.DateTimeField(default=datetime.utcnow)

    meta = {
        'indexes': [
            'email'
        ]
    }

    def __repr__(self):
        return '<Contact {}>'.format(self.email)


class AnonymousUser(AnonymousUserMixin):
    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser
