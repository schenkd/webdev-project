from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, Email, Regexp,EqualTo
from app.models import User


class LoginForm(Form):
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('passwort', validators=[DataRequired()])
    submit = SubmitField('login')


class RegisterForm(Form):
    email = StringField('email', validators=[DataRequired(), Email()])
    username = StringField('benutzername', validators=[DataRequired(), Length(min=4, max=30),
                                                   Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                          'Nur Buchstaben, Ziffern, Punkte und Unterstriche erlaubt')])
    password = PasswordField('passwort', validators=[DataRequired(),
                                                     EqualTo('password2', message='Passwörter nicht identisch.')])
    password2 = PasswordField('passwort bestätigen', validators=[DataRequired()])
    submit = SubmitField('register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('email bereits registriert')

    def validate_username(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('username existiert bereits')
