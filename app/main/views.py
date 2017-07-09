# ~*~ encoding: utf-8 ~*~
from app.main import main
from flask import render_template, request, flash, redirect, url_for
from app.main.forms import EngpassForm, ContactForm, ClassifyForm, classified
from app.models import Engpass, User, Drug, Producer, Contact, Log
from flask_login import login_required, current_user
from app.decorators import admin_required
from datetime import datetime


@main.route('/', methods=['GET', 'POST'])
def index():
    engpaesse = Engpass.objects()

    # update last seen
    if current_user.is_authenticated:
        current_user.update_last_seen()

    return render_template('main/index.html', engpaesse=engpaesse)


@main.route('/klassifizierung', methods=['GET', 'POST'])
def classify():
    form = ClassifyForm()

    # update last seen
    if current_user.is_authenticated:
        current_user.update_last_seen()

    if request.method == 'POST':
        enr = int(request.form['enr'])
        classify = int(request.form['classify'])

        try:
            # Arzneimittel klassifizierung aktualisieren
            drug = Drug.get_by_enr(enr)
            drug.update_class(classify)

            # Integer in einen String trasnformieren für die Message an den Benutzer
            classify_name = [pair[1] for pair in classified if classify in pair]
            flash('{} wurde als {} klassifiziert'.format(drug['drug_title'], classify_name[0]))

            # save in log
            user = User.objects.get(email=current_user.email)
            Log(user=user, text='{} wurde als {} klassifiziert'.format(enr, classify)).save()
        except:
            flash('ENR {} konnte keinem Arzneimittel zugewiesen werden'.format(enr))

    return render_template('hersteller/classify_form.html', form=form)


@main.route('/_getFilter', methods=['POST'])
def getFilter():
    msg = request.get_json(force=True)

    if msg == 'RELEVANT':
        print('RELEVANT')
        drugs = [doc.id for doc in Drug.objects(classify=1)]
        engpaesse = Engpass.objects(__raw__={'drug': {'$in': drugs}})
    elif msg == 'DANGER':
        print('DANGER')
        drugs = [doc.id for doc in Drug.objects(classify=2)]
        engpaesse = Engpass.objects(__raw__={'drug': {'$in': drugs}})
    else:
        print('ALL')
        engpaesse = Engpass.objects()
    print(engpaesse)
    html = render_template('main/table.html', engpaesse=engpaesse)
    return html


@main.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()

    # update last seen
    if current_user.is_authenticated:
        current_user.update_last_seen()

        # save in log
        user = User.objects.get(email=current_user.email)
        Log(user=user, category='contact', text='Hat eine Kontaktanfrage gesendet.').save()

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

        # save in log
        user = User.objects.get(email=current_user.email)
        Log(user=user, category='engpass', text='Hat einen Erstmeldung für einen Engpass gemeldet.').save()

        flash('Engpass wurde gemeldet.')
        return redirect(url_for('main.index'))
    return render_template('hersteller/engpass_form.html', form=form)


@main.route('/verwaltung', methods=['GET', 'POST'])
@login_required
@admin_required
def verwaltung():
    # update last seen
    if current_user.is_authenticated:
        current_user.update_last_seen()

    unauthorized_users = User.objects(authorized=False)
    return render_template('intern/verwaltung.html', unauthorized_users=unauthorized_users)


@main.route('/edit_engpass/<int:enr>', methods=['GET', 'POST'])
@login_required
def edit_engpass(enr):
    form = EngpassForm()
    engpass = Engpass.get_by_enr(enr)
    if request.method == 'POST':
        engpass['drug'] = Drug.objects.get(enr=int(request.form['enr']))
        print(request.form['alternative'])
        engpass['alternative'] = True if request.form['alternative'] == 'Ja' else False
        engpass['inform_expert_group'] = True if request.form['inform_expert_group'] == 'Ja' else False
        engpass['end'] = datetime(int(request.form['year']), int(request.form['month']), int(request.form['day']))
        engpass['reason'] = request.form['reason']
        engpass['other_reasons'] = request.form['other_reasons']
        engpass['telephone'] = request.form['telephone']
        engpass['email'] = request.form['email']
        engpass.update_last_report()

        # save in log
        user = User.objects.get(email=current_user.email)
        Log(user=user, category='engpass',
            text='Hat eine Zwischenmeldung für den Engpass von Arzneimittel ENR {} abgegeben.'.format(request.form['enr'])).save()

        return redirect(url_for('main.index'))
    form.enr.data = engpass.drug['enr']
    form.pzn.data = engpass.drug['pzn']
    form.alternative.default = engpass['alternative']
    form.inform_expert_group.default = engpass['inform_expert_group']
    form.day.default = engpass['end'].day
    form.month.default = engpass['end'].month
    form.year.default = engpass['end'].year
    form.reason.default = engpass['reason']
    form.other_reasons.data = engpass['other_reasons']
    form.telephone.data = engpass['telephone']
    form.email.data = engpass['email']
    return render_template('hersteller/engpass_form.html', form=form)
