# ~*~ encoding: utf-8 ~*~
from app.main import main
from flask import render_template, request, flash, redirect, url_for
from app.main.forms import EngpassForm
from app.models import Engpass, User
from flask_login import login_required, current_user
from app.decorators import admin_required


@main.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        current_user.update_last_seen()
    return render_template('main/index.html')


@main.route('/engpass', methods=['GET', 'POST'])
@login_required
def engpass():
    form = EngpassForm()
    if form.validate_on_submit():
        engpass = Engpass(
            owner='{] {}'.format(current_user.firstname, current_user.lastname),
            marketability=request.form['marketability'],
            alternative=request.form['alternative'],
            inform_expert_group=request.form['inform_expert_group'],
            hospital=request.form['hospital'],
            other_reasons=request.form['other_reasons'],
            telephone=request.form['telephon'],
            email=request.form['email'] if request.form['email'] is None else current_user.email,
            end=request.form['end'],
            enr=request.form['enr'],
            reason=request.form['reason']
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
