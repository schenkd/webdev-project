# ~*~ encoding: utf-8 ~*~
from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField, BooleanField, SubmitField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from app.models import Engpass


choices = [('-', ''),
           ('Produktionsprobleme', 'Produktionsprobleme'),
           ('Hersteller wechsel', 'Hersteller wechsel'),
           ('Änderung des Herstellungsverfahrens', 'Änderung des Herstellungsverfahrens'),
           ('Unzureichende Produktionskapazitäten', 'Unzureichende Produktionskapazitäten'),
           ('GMP-Mängel', 'GMP-Mängel'),
           ('Probleme bei der Endfreigabe', 'Probleme bei der Endfreigabe')]

boolean = [('Ja','Ja'),('Nein','Nein')]

class EngpassForm(FlaskForm):
    alternative = SelectField('Alternativen', choices=boolean)
    inform_expert_group = SelectField('Fachkreise', choices=boolean)
    hospital = SelectField('Krankhausrelevant', choices=boolean)
    other_reasons = TextAreaField('Sonstige Gruende')
    end = DateTimeField('vsl. Ende')
    enr = IntegerField('ENR', validators=[DataRequired()])
    pzn = IntegerField('PZN', validators=[DataRequired()])
    reason = SelectField('Grund für den Lieferengpass', choices=choices)
    drug_title = StringField('Bezeichnung')
    substance = StringField('Wirkstoff')
    atc_code = StringField('ATC-Code')
    marketability = SelectField('Verkehrsfaehig', choices=boolean)
    last_report = StringField('Letztes Meldedatum')
    initial_report = StringField('Datum der Erstmeldung')
    end = StringField('voraussichtliches Enddatum')
    owner = StringField('Zulassungsinhaber')
    telephon = StringField('Kontakt Telefon')
    email = StringField('Kontakt E-Mail')
    submit = SubmitField('Melden')
