# ~*~ encoding: utf-8 ~*~
from app.main import main
from flask import render_template, request, flash, redirect, url_for
from app.main.forms import EngpassForm
from app.models import Engpass, User, Drug, Producer
from flask_login import login_required, current_user
from app.decorators import admin_required
from datetime import datetime


@main.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        current_user.update_last_seen()
    return render_template('main/index.html')


@main.route('/engpass', methods=['GET', 'POST'])
@login_required
def engpass():
    form = EngpassForm()
    if request.method == 'POST' and form.validate_on_submit():
        engpass = Engpass(
            producer=Producer.objects.get(employee=User.objects.get(email=current_user.email)),
            drug=Drug.objects.get(enr=request.form['enr']),
            pzn=request.form['pzn'],
            alternative=request.form['alternative'],
            inform_expert_group=request.form['inform_expert_group'],
            telephone=request.form['telephon'],
            email=request.form['email'] if request.form['email'] is None else current_user.email,
            end=datetime(request.form['year'], request.form['month'], request.form['day']),
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
