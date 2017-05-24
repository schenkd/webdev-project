# ~*~ encoding: utf-8 ~*~
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo


class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('passwort', validators=[DataRequired()])
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email()])
    username = StringField('benutzername', validators=[DataRequired(), Length(min=4, max=30),
                                                   Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                          'Nur Buchstaben, Ziffern, Punkte und Unterstriche erlaubt')])
    password = PasswordField('passwort', validators=[DataRequired(),
                                                     EqualTo('password2', message='Passwörter nicht identisch.')])
    password2 = PasswordField('passwort bestätigen', validators=[DataRequired()])
    submit = SubmitField('register')
