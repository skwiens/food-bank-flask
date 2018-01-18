from flask import render_template, session, flash, redirect, url_for, request
from app import app

import os
import google_auth_oauthlib.flow
import google.oauth2.credentials
import googleapiclient.discovery

# CLIENT_SECRETS_FILE = os.environ['CLIENT_SECRETS_FILE']
CLIENT_SECRETS_FILE = 'client_secret.json'
CLIENT_SECRET = os.environ['CLIENT_SECRET']
CLIENT_SECRET = os.environ['CLIENT_SECRET']
SCOPES = ['https://www.googleapis.com/auth/gmail.compose', 'https://www.googleapis.com/auth/calendar']
APPLICATION_NAME='Bethany Food Bank'

def credentials_to_dict(credentials):
  return {'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': credentials.scopes}

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')







@app.route('/admin_login')
def admin_login():
    if 'credentials' not in session:
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

@app.route('/authorize')
def authorize():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
      CLIENT_SECRETS_FILE, scopes=SCOPES)

    flow.redirect_uri = url_for('oauth2callback', _external=True)

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true')

    session['state'] = state

    return redirect(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
    state = session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
      CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = url_for('oauth2callback', _external=True)

    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    session['credentials'] = credentials_to_dict(credentials)

    return redirect(url_for('admin_login'))
