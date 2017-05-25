# ~*~ encoding: utf-8 ~*~
from app.auth import auth
from app.models import User
from app.auth.forms import LoginForm, RegisterForm
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects.get(email=request.form['email'])
        if user is not None and user.verify_password(request.form['password']):
            login_user(user)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Ungültiger Benutzername oder Passwort')
    return render_template('auth/login.html', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password_hash=User.generate_password(form.password.data))
        user.save()
        flash('Willkommen {}!'.format(user.username))
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)


@auth.route('/logout', methods=['GET'])
def logout():
    logout_user()
    flash('Auf Wiedersehen!')
    return redirect(url_for('main.index'))
