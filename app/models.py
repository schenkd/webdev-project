from app import db, login_manager
from flask_login import UserMixin, AnonymousUserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    """ Standard User Model """
    __tablename__ = 'users'

    # Spalten der SQL DB
    id = db.Column(db.Intger, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(30), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    member_since = db.Column(db.DateTime(), default=datetime.utcnow())
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow())

    # Zum tracken wann der User das letzte mal auf der Homepage war
    def update_last_seen(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    # Security: Passwort auslesen unzulässig
    @property
    def password(self):
        raise AttributeError('passwort ist nicht lesbar')

    # Security: Passwort wird gehasht
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # Security: Passwort wird mittels Methode geprüft
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Debugging: Beschreibung des Objekts
    def __repr__(self):
        return 'User\nUsername: {]\nEmail: {}'.format(self.username, self.email)


class AnonymousUser(AnonymousUserMixin):
    """ Anonymous User Model """
    # Hier können uns noch ein paar Dinge überlegen für den Anonymous
    pass

# Nicht eingeloggte User erhalten automatisch das Anonymous User Model
login_manager.anonymous_user = AnonymousUser
