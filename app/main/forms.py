# ~*~ encoding: utf-8 ~*~
from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField, BooleanField, SubmitField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from app.models import Engpass
from datetime import datetime


def generate_int_tupel_list(number):
    liste = list()
    for x in range(1, number+1):
        liste.append((x, str(x)))
    return liste


def get_date():
    date = datetime.date(datetime.utcnow())
    return {'year': date.year, 'month': date.month, 'day': date.day}


choices = [('None', ''),
           ('Produktionsprobleme', 'Produktionsprobleme'),
           ('Hersteller wechsel', 'Hersteller wechsel'),
           ('Änderung des Herstellungsverfahrens', 'Änderung des Herstellungsverfahrens'),
           ('Unzureichende Produktionskapazitäten', 'Unzureichende Produktionskapazitäten'),
           ('GMP-Mängel', 'GMP-Mängel'),
           ('Probleme bei der Endfreigabe', 'Probleme bei der Endfreigabe')]

boolean = [(True, 'Ja'),
           (False, 'Nein')]

day = generate_int_tupel_list(31)
month = generate_int_tupel_list(12)
year = [(2017, '2017'),
        (2018, '2018'),
        (2019, '2019')]


class EngpassForm(FlaskForm):
    pzn = IntegerField('PZN')
    alternative = SelectField('Alternativepräperate', choices=boolean, default=False)
    inform_expert_group = SelectField('Info an Fachkreise', choices=boolean, default=False)
    hospital = SelectField('Krankhausrelevant', choices=boolean, default=False)
    other_reasons = TextAreaField('Sonstige Gründe')
    telephon = StringField('Telefon')
    email = StringField('Email')
    day = SelectField('Tag', choices=day, default=get_date()['day'])
    month = SelectField('Monat', choices=month, default=get_date()['month'])
    year = SelectField('Jahr', choices=year, default=get_date()['year'])
    enr = IntegerField('ENR', validators=[DataRequired()])
    reason = SelectField('Grund für den Lieferengpass', choices=choices)
    submit = SubmitField('Melden')
