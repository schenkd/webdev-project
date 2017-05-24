# ~*~ encoding: utf-8 ~*~
from app import db, login_manager
from datetime import datetime
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Berechtigung:
    FAVOURITE = 0x01
    WRITE_ENGPASS = 0x04
    MODERATE = 0x08
    FACHABTEILUNG = 0x80


class User(UserMixin, db.Document):
    """ Modell für den Standard-User """
    email = db.EmailField(required=True, unique=True)
    password_hash = db.StringField()
    user_name = db.StringField(max_length=50, required=True, unique=True)
    first_name = db.StringField(max_length=50)
    last_name = db.StringField(max_length=50)
    member_since = db.DateTimeField(default=datetime.utcnow)
    last_seen = db.DateTimeField(default=datetime.utcnow)

    meta = {
        'indexes': ['email', 'user_name']
    }

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.User.save(self)

    @property
    def password(self):
        raise AttributeError('Passwort ist nicht lesbar!')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return 'User %r' % self.user_name


class Arzneimittel(db.Document):
    """ Modell für die Arzneimittel """
    pzn = db.DecimalField(required=True, unique=True)
    name = db.StringField(required=True, unique=True)
    beschreibung = db.StringField()
    hersteller = db.StringField(required=True)
    gruppe = db.StringField(required=True)
    keywords = db.ListField()
    wirkstoff = db.ListField(required=True)
    darreichungsform = db.StringField()

    meta = {
        'indexes': ['pzn', 'name', 'supplier', 'group', 'keywords', 'substance']
    }

    def __repr__(self):
        return 'Arzneimittel %r' % self.name


class Engpass(db.Document):
    """ Modell für die gemeldeten Engpässe """
    autor = db.ReferenceField(User)
    meldung = db.StringField()
    status = db.IntField(required=True)
    start = db.DateTimeField(default=datetime.utcnow)
    ende = db.DateTimeField()
    arzneimittel = db.ReferenceField(Arzneimittel)

    meta = {
        'indexes': ['start', 'arzneimittel']
    }

    def __repr__(self):
        return 'Engpass von %r' % self.autor


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser
