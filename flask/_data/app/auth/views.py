# ~*~ encoding: utf-8 ~*~
from app.auth import auth
from app.models import User, Producer
from app.auth.forms import LoginForm, RegisterFormExtern, RegisterFormIntern
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user
from mongoengine.errors import NotUniqueError
from app.decorators import admin_required


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


@auth.route('/extern', methods=['GET', 'POST'])
def extern():
    form = RegisterFormExtern()
    if request.method == 'POST' and form.validate_on_submit():
        user = User(email=request.form['email'],
                    firstname=request.form['firstname'],
                    lastname=request.form['lastname'],
                    password_hash=User.generate_password(request.form['password']),
                    permission='Hersteller')
        try:
            user.save()
            # Referenzierung zum Zulassungsinhaber
            producer = Producer.objects.get(pnr=request.form['pnr'])
            producer['employee'] += [User.objects.get(email=request.form['email'])]
            producer.save()
        except NotUniqueError:
            flash('NotUniqueError!')
        flash('Willkommen {}!'.format(user.firstname))
        return redirect(url_for('main.index'))
    return render_template('auth/extern.html', form=form)


@auth.route('/intern', methods=['GET', 'POST'])
def intern():
    form = RegisterFormIntern()
    if request.method == 'POST' and form.validate_on_submit():
        user = User(email=request.form['email'],
                    firstname=request.form['firstname'],
                    lastname=request.form['lastname'],
                    password_hash=User.generate_password(request.form['password']),
                    permission='Fachabteilung',
                    department=request.form['department'],
                    room=request.form['room'],
                    personal_number=request.form['personal_number'])
        try:
            user.save()
        except NotUniqueError:
            flash('NotUniqueError!')
        flash('Willkommen {}!'.format(user.firstname))
        return redirect(url_for('main.index'))
    return render_template('auth/intern.html', form=form)


@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash('Auf Wiedersehen!')
    return redirect(url_for('main.index'))


@auth.route('/approval', methods=['POST'])
@login_required
@admin_required
def approval():
    user = User.objects.get(email=request.form['email'])
    if request.form['approval'] == 'True':
        user.authorized = True
        user.save()
    elif request.form['approval'] == 'False':
        user.delete()
    return redirect(url_for('main.verwaltung'))
