# ~*~ encoding: utf-8 ~*~
from app.main import main
from flask import render_template, request, flash, redirect, url_for
from app.main.forms import EngpassForm, ContactForm
from app.models import Engpass, User, Drug, Producer, Contact
from flask_login import login_required, current_user
from app.decorators import admin_required
from datetime import datetime


@main.route('/', methods=['GET', 'POST'])
def index():
    engpaesse =Engpass.objects()
    if current_user.is_authenticated:
        current_user.update_last_seen()
    return render_template('main/index.html', engpaesse=engpaesse)


@main.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if current_user.is_authenticated:
        current_user.update_last_seen()
    if request.method == 'POST' and form.validate_on_submit():
        contact = Contact(firstname=request.form['firstname'],
                          lastname=request.form['lastname'],
                          telephone=request.form['telephone'],
                          message=request.form['message'],
                          email=request.form['email'])
        contact.save()
        flash('Ihre Nachricht wurde erfolgreich übermittelt.')
    return render_template('main/contact.html', form=form)


@main.route('/engpass', methods=['GET', 'POST'])
@login_required
def engpass():
    form = EngpassForm()
    # TODO: Form validierung funktioniert noch nicht!
    if request.method == 'POST':
        engpass = Engpass(
            producer=Producer.get_by_employee(current_user.email),
            drug=Drug.get_by_enr(int(request.form['enr'])),
            alternative=request.form['alternative'],
            inform_expert_group=request.form['inform_expert_group'],
            telephone=request.form['telephone'],
            email=request.form['email'] if request.form['email'] is None else current_user.email,
            end=datetime(int(request.form['year']), int(request.form['month']), int(request.form['day'])),
            reason=request.form['reason'],
            other_reasons=request.form['other_reasons']
        )
        engpass.save()
        flash('Engpass wurde gemeldet.')
        return redirect(url_for('main.index'))
    return render_template('hersteller/engpass_form.html', form=form)


@main.route('/verwaltung', methods=['GET', 'POST'])
@login_required
@admin_required
def verwaltung():
    unauthorized_users = User.objects(authorized=False)
    return render_template('intern/verwaltung.html', unauthorized_users=unauthorized_users)
