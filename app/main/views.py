# ~*~ encoding: utf-8 ~*~
from . import main
from flask import flash, redirect, render_template, request, url_for
from flask_login import (current_user, login_required, login_user, logout_user)
from .forms import (LoginForm)


@main.route('/login', methods=['GET', 'POST'])
def login():
    """Log in an existing user."""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.password_hash is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash('You are now logged in. Welcome back!', 'success')
            return redirect(request.args.get('main/index.html'))
        else:
            flash('Invalid email or password.', 'form-error')
    return render_template('main/login.html', form=form)


@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return render_template('main/index.html')


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('main/index.html')
