# ~*~ encoding: utf-8 ~*~
from app.main import main
from flask import render_template, request, flash, redirect, url_for
from app.main.forms import EngpassForm
from app.models import Engpass, User
from flask_login import login_required, current_user


@main.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        current_user.update_last_seen()
    engpaesse = Engpass.objects(marketability='Ja')
    return render_template('main/index.html', engpaesse=engpaesse)


@main.route('/engpass', methods=['GET', 'POST'])
@login_required
def engpass():
    form = EngpassForm()
    if form.validate_on_submit():
        engpass = Engpass(enr=request.form['enr'],pzn=request.form['pzn'],email=request.form['email'],telephon=request.form['telephon'],owner=request.form['owner'],other_reasons=request.form['other_reasons'],reason=request.form['reason'],end=request.form['end'],initial_report=request.form['initial_report'],last_report=request.form['last_report'],hospital=request.form['hospital'],alternative=str(request.form['alternative'] or 'n'),marketability=str(request.form['marketability'] or 'n'),inform_expert_group=str(request.form['inform_expert_group'] or 'n'),drug_title=request.form['drug_title'],substance=request.form['substance'],atc_code=request.form['atc_code'])
        engpass.save()
        flash('Engpass wurde gemeldet.')
        return redirect(url_for('main.index'))
    return render_template('hersteller/engpass_form.html', form=form)


@main.route('/verwaltung', methods=['GET', 'POST'])
@login_required
def verwaltung():
    if current_user.is_authenticated and current_user.permission == '1':
        unauthorized_users = User.objects(authorized=False)
        return render_template('intern/verwaltung.html', unauthorized_users=unauthorized_users)
    else:
        return render_template('main/index.html')
