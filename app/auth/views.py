# ~*~ encoding: utf-8 ~*~
from app.auth import auth
from app.models import User
from app.auth.forms import LoginForm, RegisterForm
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user
from mongoengine.errors import NotUniqueError


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.objects.get(email=request.form['email'])
        if user is not None and user.verify_password(request.form['password']):
            if user.authorized:
                login_user(user)
                return redirect(request.args.get('next') or url_for('main.index'))
            flash('Sorry, ihr Account wurde noch nicht autorisiert.')
    else:
        flash('Bitte überprüfen Sie ihre Zugangsdaten.')
    return render_template('auth/login.html', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User(email=request.form['email'],
                    firstname=request.form['firstname'],
                    lastname=request.form['lastname'],
                    password_hash=User.generate_password(request.form['password']),
                    permission=request.form['permission'])
        try:
            user.save()
        except NotUniqueError:
            flash('NotUniqueError!')
        flash('Willkommen {}!'.format(user.firstname))
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)


@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash('Auf Wiedersehen!')
    return redirect(url_for('main.index'))
