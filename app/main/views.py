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


@main.route('/search/<query>', methods=['GET', 'POST'])
def search_query(query):
    pass


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

            # Integer in einen String transformieren
            # als Text in der Message und im Log
            classify_name = [pair[1] for pair in classified if classify in pair]
            flash('{} wurde als {} klassifiziert'.format(drug['drug_title'], classify_name[0]))

            # save in log
            user = User.objects.get(email=current_user.email)
            Log(user=user, category='classify', text='{} wurde als {} klassifiziert'.format(enr, classify)).save()
        except:
            flash('ENR {} konnte keinem Arzneimittel zugewiesen werden'.format(enr))

    # query Arzneimittel entsprechend der Klassifizierung
    relevants = Drug.objects(classify=1)
    dangers = Drug.objects(classify=2)

    return render_template('intern/classify/form.html', form=form, relevants=relevants, dangers=dangers)


@main.route('/_getFilter', methods=['POST'])
def getFilter():
    msg = request.get_json(force=True)

    if msg == 'RELEVANT':
        # query alle versorgungsrelevanten Engpaesse
        drugs = [doc.id for doc in Drug.objects(classify=1)]
        engpaesse = Engpass.objects(__raw__={'drug': {'$in': drugs}})
    elif msg == 'DANGER':
        # query alle versorgungsgefährdende Engpaesse
        drugs = [doc.id for doc in Drug.objects(classify=2)]
        engpaesse = Engpass.objects(__raw__={'drug': {'$in': drugs}})
    else:
        # query alle Engpaesse
        engpaesse = Engpass.objects()

    return render_template('main/table.html', engpaesse=engpaesse)


@main.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()

    # update last seen
    if current_user.is_authenticated:
        current_user.update_last_seen()

    if request.method == 'POST' and form.validate_on_submit():
        # Erstellen eines Contact Dokument
        Contact(firstname=request.form['firstname'],
                lastname=request.form['lastname'],
                telephone=request.form['telephone'],
                message=request.form['message'],
                email=request.form['email']
                ).save()

        # save in log
        user = User.objects.get(email=current_user.email)
        Log(user=user, category='contact', text='Hat eine Kontaktanfrage gesendet.').save()

        flash('Ihre Nachricht wurde erfolgreich übermittelt.')
    return render_template('main/contact.html', form=form)


@main.route('/engpass', methods=['GET', 'POST'])
@login_required
def engpass():
    form = EngpassForm()

    if request.method == 'POST':
        # Erststellung eines Engpass Document
        Engpass(
            producer=Producer.get_by_employee(current_user.email),
            drug=Drug.get_by_enr(int(request.form['enr'])),
            alternative=request.form['alternative'],
            inform_expert_group=request.form['inform_expert_group'],
            telephone=request.form['telephone'],
            email=request.form['email'] if request.form['email'] is None else current_user.email,
            end=datetime(int(request.form['year']), int(request.form['month']), int(request.form['day'])),
            reason=request.form['reason'],
            other_reasons=request.form['other_reasons']
        ).save()

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

    # query aller nicht autorisierten User
    unauthorized_users = User.objects(authorized=False)

    # query letzten Zehn Log Documents
    logs = Log.objects[:10]

    return render_template('intern/admin/verwaltung.html', unauthorized_users=unauthorized_users, logs=logs)


@main.route('/edit_engpass/<int:enr>', methods=['GET', 'POST'])
@login_required
def edit_engpass(enr):
    form = EngpassForm()

    # Ausgewählte Engpass Document laden
    engpass = Engpass.get_by_enr(enr)

    if request.method == 'POST':
        # Bearbeitung des Engpass Document
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

    # Zuweisung der Values aus dem Engpass Document
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
