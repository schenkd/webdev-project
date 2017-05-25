# ~*~ encoding: utf-8 ~*~
from app.main import main
from flask import render_template, request, flash, redirect, url_for
from app.main.forms import EngpassForm
from app.models import Engpass
from flask_login import login_required


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@main.route('/engpass', methods=['GET', 'POST'])
def engpass():
    form = EngpassForm()
    if form.validate_on_submit():
        engpass = Engpass(
            marketability=request.form['marketability'],
            alternative=request.form['alternative'],
            inform_expert_group=request.form['inform_expert_group'],
            hospital=request.form['hospital'],
            other_reasons=request.form['other_reasons'],
            telephon=request.form['telephon'],
            email=request.form['email'],
            end=request.form['end'],
            enr=request.form['enr'],
            reason=request.form['reason']
        )
        engpass.save()
        flash('Engpass wurde gemeldet.')
        return redirect(url_for('main.index'))
    return render_template('engpass.html', form=form)
