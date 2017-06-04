# ~*~ encoding: utf-8 ~*~
from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField, BooleanField, SubmitField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from app.models import Engpass


choices = [('None', ''),
           ('Produktionsprobleme', 'Produktionsprobleme'),
           ('Hersteller wechsel', 'Hersteller wechsel'),
           ('Änderung des Herstellungsverfahrens', 'Änderung des Herstellungsverfahrens'),
           ('Unzureichende Produktionskapazitäten', 'Unzureichende Produktionskapazitäten'),
           ('GMP-Mängel', 'GMP-Mängel'),
           ('Probleme bei der Endfreigabe', 'Probleme bei der Endfreigabe')]

boolean = [(True, 'Ja'),
           (False, 'Nein')]


class EngpassForm(FlaskForm):
    # TODO: PZN hinzufügen + marketability weg
    marketability = SelectField('Verkehrsfähig', choices=boolean)
    alternative = SelectField('Alternativepräperate', choices=boolean)
    inform_expert_group = SelectField('Info an Fachkreise', choices=boolean)
    hospital = SelectField('Krankhausrelevant', choices=boolean)
    other_reasons = TextAreaField('Sonstige Gründe')
    telephon = StringField('Telefon')
    email = StringField('Email')
    # TODO: Muss noch geändert werden in Day, Month, Year Field
    end = DateTimeField('vsl. Ende')
    enr = IntegerField('ENR', validators=[DataRequired()])
    reason = SelectField('Grund für den Lieferengpass', choices=choices)
    submit = SubmitField('Melden')
