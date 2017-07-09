# ~*~ encoding: utf-8 ~*~
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, ValidationError
from datetime import datetime
from app.models import Drug


# Generiert ein Liste von Tupeln aus einem integer und einem string
def generate_int_tupel_list(number):
    liste = list()
    for x in range(1, number+1):
        liste.append((x, str(x)))
    return liste


def get_date():
    date = datetime.date(datetime.utcnow())
    return {'year': date.year, 'month': date.month, 'day': date.day}


choices = [(None, ''),
           ('Produktionsprobleme', 'Produktionsprobleme'),
           ('Hersteller wechsel', 'Hersteller wechsel'),
           ('Änderung des Herstellungsverfahrens', 'Änderung des Herstellungsverfahrens'),
           ('Unzureichende Produktionskapazitäten', 'Unzureichende Produktionskapazitäten'),
           ('GMP-Mängel', 'GMP-Mängel'),
           ('Probleme bei der Endfreigabe', 'Probleme bei der Endfreigabe')]

boolean = [(False, 'Nein'),
           (True, 'Ja')]

day = generate_int_tupel_list(31)
month = generate_int_tupel_list(12)
year = [(2017, '2017'),
        (2018, '2018'),
        (2019, '2019')]

classified = [(0, 'keine Klassifizierung'),
              (1, 'versorgungsrelevant'),
              (2, 'versorgungsgefährdend')]


class EngpassForm(FlaskForm):
    enr = IntegerField('ENR', validators=[DataRequired()])
    pzn = IntegerField('PZN')
    alternative = SelectField('Alternativepräperate', choices=boolean, default=False)
    inform_expert_group = SelectField('Info an Fachkreise', choices=boolean, default=False)
    day = SelectField('Tag', choices=day, default=get_date()['day'])
    month = SelectField('Monat', choices=month, default=get_date()['month'])
    year = SelectField('Jahr', choices=year, default=get_date()['year'])
    reason = SelectField('Grund für den Lieferengpass', choices=choices)
    other_reasons = TextAreaField('Sonstige Gründe')
    telephone = StringField('Telefon')
    email = StringField('Email')
    submit = SubmitField('Melden')

    def validate_enr(self, field):
        print('VALIDATION')
        if not Drug.objects(enr=self.enr.data):
            print('ERROR!')
            raise ValidationError('ENR ist nicht bekannt!')


class ContactForm(FlaskForm):
    firstname = StringField('Vorname', validators=[DataRequired()])
    lastname = StringField('Nachname', validators=[DataRequired()])
    message = TextAreaField('Nachricht')
    telephone = StringField('Telefon')
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Abschicken')


class ClassifyForm(FlaskForm):
    enr = IntegerField('ENR', validators=[DataRequired()])
    classify = SelectField('Klassifizierung', choices=classified)
    submit = SubmitField('Abschicken')
