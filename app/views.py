from flask import render_template, session, flash, redirect, url_for, request
from app import app
from app.oauth_helpers import *

import os
import httplib2
import google_auth_oauthlib.flow
import google.oauth2.credentials
import googleapiclient.discovery

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/admin_login')
def admin_login():
    if 'credentials' not in session:
        print('credentials not in session')
        return redirect('authorize')

    # Load credentials from the session.
    credentials = google.oauth2.credentials.Credentials(
      **session['credentials'])

    service = googleapiclient.discovery.build(
      'gmail', 'v1', credentials=credentials)

    if service:
        user_profile = service.users().getProfile(userId='me').execute()
        emailAddress = user_profile['emailAddress']
        if user_profile['emailAddress'] == 'xana.wines.ada@gmail.com':
            session['user']='admin'
            flash('You are now logged in as an administrator', 'success')
            # redirect(url_for('index'))
        else:
            flash('You do not have admin privileges, please contact Bethany Food Bank if you have any questions', 'danger')
            redirect(url_for('clear'))
    else:
        flash('Sorry! Something went wrong. Please try again in a few moments', 'danger')


    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    if 'credentials' in session:
        del session['credentials']
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('index'))
