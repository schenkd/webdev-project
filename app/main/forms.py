# ~*~ encoding: utf-8 ~*~
from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField, BooleanField, SubmitField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from app.models import Engpass


choices = [('Produktionsprobleme', 'Produktionsprobleme'),
           ('Hersteller wechsel', 'Hersteller wechsel'),
           ('Änderung des Herstellungsverfahrens', 'Änderung des Herstellungsverfahrens'),
           ('Unzureichende Produktionskapazitäten', 'Unzureichende Produktionskapazitäten'),
           ('GMP-Mängel', 'GMP-Mängel'),
           ('Probleme bei der Endfreigabe', 'Probleme bei der Endfreigabe')]


class EngpassForm(FlaskForm):
    marketability = BooleanField('Verkehrsfähig', validators=[DataRequired()])
    alternative = BooleanField('Alternativepräperate', validators=[DataRequired()])
    inform_expert_group = BooleanField('Info an Fachkreise', validators=[DataRequired()])
    hospital = BooleanField('Krankhausrelevant', validators=[DataRequired()])
    other_reasons = TextAreaField('Sonstige Gründe')
    telephon = StringField('Telefon')
    email = StringField('Email')
    end = DateTimeField('vsl. Ende')
    enr = IntegerField('ENR', validators=[DataRequired()])
    reason = SelectField('Grund für den Lieferengpass', choices=choices)
    submit = SubmitField('Melden')
