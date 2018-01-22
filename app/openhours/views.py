#app/openhours/views.py

from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from app import db
from app.models import Openhour, Volunteer, Note
from app.forms import OpenhourForm, NoteForm
from app.email_helpers import *

import os
import googleapiclient.discovery
import google.oauth2.credentials
import datetime

ADMIN_EMAIL = os.environ['ADMIN_EMAIL']

openhours_blueprint = Blueprint('openhours', __name__, template_folder='templates')

@openhours_blueprint.route('/')
def index():
    openhours = Openhour.query.all()

    if openhours:
        return render_template('openhours.html', openhours=openhours)
    else:
        msg = 'No Open Hours Found'
        return render_template('openhours.html', msg=msg)

@openhours_blueprint.route('/new', methods=['GET', 'POST'])
# @admin_logged_in
def new_openhour():
    form = OpenhourForm(request.form)

    # Dynamically create a list of volunteers to select for the openhour
    volunteer_list = [(volunteer.id, volunteer.name) for volunteer in Volunteer.query.filter(Volunteer.role != 'shopper').all()]
    form.volunteers.choices = volunteer_list
    form.volunteers.choices.insert(0, (-1, 'None'))

    shopper_list = [(volunteer.id, volunteer.name) for volunteer in Volunteer.query.filter(Volunteer.role != 'open-hours').all()]
    form.shoppers.choices = shopper_list
    form.shoppers.choices.insert(0, (-1, 'None'))

    if request.method == 'POST' and form.validate():
        new_openhour = Openhour(date=form.date.data)
        db.session.add(new_openhour)

        # Add in any volunteers and shoppers
        for volunteer in form.volunteers.data:
            if volunteer != -1:
                new_openhour.volunteers.append(Volunteer.query.get(volunteer))

        for shopper in form.shoppers.data:
            if volunteer != -1:
                new_openhour.shoppers.append(Volunteer.query.get(shopper))

        db.session.commit()

        flash('Record for %s saved!' % new_openhour.date.strftime('%m/%d/%Y'), 'success')

        return redirect(url_for('index'))

    return render_template('openhour_form.html', form=form)

@openhours_blueprint.route('/<string:id>/edit', methods=['GET', 'POST'])
# @admin_logged_in
def edit_openhour(id):

    openhour = Openhour.query.get(id)
    form = OpenhourForm(request.form, obj=openhour)

    #Dynamically create a list of volunteers to select for the openhour
    volunteer_list = [(volunteer.id, volunteer.name) for volunteer in Volunteer.query.filter(Volunteer.role != 'shopper').all()]
    form.volunteers.choices = volunteer_list
    form.volunteers.choices.insert(0, (-1, 'None'))

    shopper_list = [(volunteer.id, volunteer.name) for volunteer in Volunteer.query.filter(Volunteer.role != 'open-hours').all()]
    form.shoppers.choices = shopper_list
    form.shoppers.choices.insert(0, (-1, 'None'))

    if request.method == 'POST' and form.validate():
        openhour.date=form.date.data
        openhour.volunteers = []
        openhour.shoppers = []

        for volunteer in form.volunteers.data:
            if volunteer != -1:
                openhour.volunteers.append(Volunteer.query.get(volunteer))

        for shopper in form.shoppers.data:
            if shopper != -1:
                openhour.shoppers.append(Volunteer.query.get(shopper))

        db.session.commit()

        flash('Information for %s Updated' % openhour.date.strftime('%b %d, %Y'), 'success')

        return redirect(url_for('openhours.index'))
    else:
        return render_template('openhour_form.html', form=form)

@openhours_blueprint.route('/<string:id>/post', methods=['GET', 'POST'])
# @admin_logged_in
def post_openhour(id):
    credentials = google.oauth2.credentials.Credentials(**session['credentials'])
    service = googleapiclient.discovery.build('calendar', 'v3', credentials=credentials)

    openhour = Openhour.query.get(id)
    date = '{:%Y-%m-%d}'.format(openhour.date)

    for volunteer in openhour.volunteers:
        # Post to calendar
        event = {
            'summary': 'OH: %s' % volunteer.name,
            'start': {
                'date': date
            },
            'end': {
                'date': date
            }
        }
        event = service.events().insert(calendarId='primary', body=event).execute()
        print ('Event created: %s' % (event.get('htmlLink')))

        # Send email to volunteer
        sender = ADMIN_EMAIL
        to = volunteer.email
        subject = 'Volunteer Bethany Food Bank %s' % openhour.date.strftime('%b %d')
        msgHtml = render_template('schedule_email.html', volunteer=volunteer.name, date=openhour.date.strftime('%b %d'))
        msgPlain = render_template('schedule_email.txt', volunteer=volunteer.name, date=openhour.date.strftime('%b %d'))

        SendMessage(sender, to, subject, msgHtml, msgPlain)

    # Increase date by one day to see easier on the calendar
    shopdate = openhour.date + datetime.timedelta(days=1)
    date = '{:%Y-%m-%d}'.format(shopdate)

    for shopper in openhour.shoppers:
        event = {
            'summary': 'SHOP: %s' % shopper.name,
            'start': {
                'date': date
            },
            'end': {
                'date': date
            }
        }
        event = service.events().insert(calendarId='primary', body=event).execute()
        print ('Event created: %s' % (event.get('htmlLink')))

        # Send email to shopper
        sender = ADMIN_EMAIL
        to = shopper.email
        subject = 'Shop week of  %s for Bethany Food Bank' % openhour.date.strftime('%m/%d/%Y')
        msgHtml = render_template('shop_schedule_email.html', shopper=shopper.name, date=openhour.date.strftime('%b %d'))
        msgPlain = render_template('shop_schedule_email.txt', shopper=shopper.name, date=openhour.date.strftime('%b %d'))

        SendMessage(sender, to, subject, msgHtml, msgPlain)

    return redirect(url_for('openhours.index'))

@openhours_blueprint.route('/<string:id>/notes/new', methods=['GET', 'POST'])
def new_notes(id):
    form = NoteForm(request.form)
    form.author.choices = [(volunteer.id, volunteer.name) for volunteer in Volunteer.query.all()]
    form.author.choices.insert(0, (-1, 'Select your name'))

    openhour = Openhour.query.get(id)

    if request.method == 'POST' and form.validate():
        new_note = Note(
            openhour_id = id,
            author = form.author.data,
            customers = form.customers.data,
            body = form.body.data,
            shopping = form.shopping.data
        )

        db.session.add(new_note)
        db.session.commit()

        # Send email based on the Notes
        ##[ ] Turn this email msg into a template version to send
        # sender = 'xana.wines@gmail.com'
        # subject = 'Open Hour: ' + openhour.date.strftime('%m/%d/%Y')
        # msgHtml = new_note.shopping
        # msgPlain = new_note.shopping
        # recipients = []
        #
        # for volunteer in openhour.volunteers:
        #     recipients.append(volunteer.email)
        #
        # to = ','.join(recipients)
        #
        # SendMessage(sender, to, subject, msgHtml, msgPlain)

        flash('Notes created for %s. Thank you for volunteering tonight!' % openhour.date.strftime('%m/%d/%Y'), 'success')

        return redirect(url_for('index'))

    return render_template('notes_form.html', form=form)

@openhours_blueprint.route('/<string:id>/notes')
def notes(id):
    openhour = Openhour.query.get(id)
    notes = openhour.notes[0]
    author = Volunteer.query.get(notes.author)

    return render_template('notes.html', notes=notes, openhour=openhour, author=author)
