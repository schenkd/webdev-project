# ~*~ encoding: utf-8 ~*~
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField, DateTimeField, BooleanField, SubmitField, TextAreaField, IntegerField, SelectField, ValidationError
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from app.models import User

choices = [('Hersteller', 'Hersteller'),
           ('Fachabteilung', 'Fachabteilung')]


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Passwort', validators=[DataRequired()])
    submit = SubmitField('Login')

    def validate_email(self, field):
        if not User.objects(email=self.email.data):
            raise ValidationError('Email ist nicht korrekt!')


class RegisterFormExtern(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    firstname = StringField('Vorname', validators=[DataRequired()])
    lastname = StringField('Nachname', validators=[DataRequired()])
    password = PasswordField('Passwort', validators=[DataRequired(),EqualTo('password2', message='Passwörter nicht identisch.')])
    password2 = PasswordField('Passwort bestätigen', validators=[DataRequired()])
    permission = SelectField('Berechtigung', choices=choices, validators=[DataRequired()])
    pnr = IntegerField('PNR')
    submit = SubmitField('Register')

class RegisterFormIntern(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    firstname = StringField('Vorname', validators=[DataRequired()])
    lastname = StringField('Nachname', validators=[DataRequired()])
    password = PasswordField('Passwort', validators=[DataRequired(),EqualTo('password2', message='Passwörter nicht identisch.')])
    password2 = PasswordField('Passwort bestätigen', validators=[DataRequired()])
    permission = SelectField('Berechtigung', choices=choices, validators=[DataRequired()])
    department = StringField('Abteilung')
    room = StringField('Raum')
    personal_number = StringField('Stellenzeichen')
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.objects(email=self.email.data):
            raise ValidationError('Email bereits vergeben!')
