# ~*~ encoding: utf-8 ~*~
from app.auth import auth
from flask import render_template
from app.auth.forms import LoginForm


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('auth/login.html', form=form)
