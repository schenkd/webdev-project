# ~*~ encoding: utf-8 ~*~
from app import db, login_manager
from datetime import datetime
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Document):
    """ Modell für den Standard-User """
    __collection__ = 'user'
    structure = {
        'email': db.unicode,
        'username': db.unicode,
        'password_hash': db.unicode,
        'firstname': db.unicode,
        'lastname': db.unicode,
        'member_since': db.datetime,
        'last_seen': db.datetime
    }
    required_fields = ['email', 'password_hash', 'username']
    default_values = {'member_since': datetime.utcnow()}
    use_dot_notation = True

    def ping(self):
        self.last_seen = datetime.utcnow()
        self.save()

    @property
    def password(self):
        raise AttributeError('Passwort ist nicht lesbar!')

    def password_hash(self, password):
        return generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username


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

# For using the document model we must register it with the connection
db.register([User])