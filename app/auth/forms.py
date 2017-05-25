# ~*~ encoding: utf-8 ~*~
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, ValidationError
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from app.models import User


choices = [('0', 'Hersteller'),
           ('1', 'Fachabteilung')]


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Passwort', validators=[DataRequired()])
    submit = SubmitField('Login')

    def validate_email(self, field):
        if not User.objects(email=self.email.data):
            raise ValidationError('Email ist nicht korrekt!')


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    firstname = StringField('Vorname', validators=[DataRequired()])
    lastname = StringField('Nachname', validators=[DataRequired()])
    password = PasswordField('Passwort', validators=[DataRequired(),
                                                     EqualTo('password2', message='Passwörter nicht identisch.')])
    password2 = PasswordField('Passwort bestätigen', validators=[DataRequired()])
    permission = SelectField('Berechtigung', choices=choices, validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.objects(email=self.email.data):
            raise ValidationError('Email bereits vergeben!')
