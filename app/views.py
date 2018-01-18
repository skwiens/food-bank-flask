from flask import render_template, session, flash, redirect, url_for, request
from app import app
from app.oauth_helpers import *


from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import os
import httplib2
import google_auth_oauthlib.flow
import google.oauth2.credentials
import googleapiclient.discovery

# try:
#     import argparse
#     flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
# except ImportError:
#     flags = None

# CLIENT_SECRET_FILE = 'client_secret.json'
CLIENT_SECRET_FILE = os.environ['CLIENT_SECRET_FILE']
CLIENT_ID = os.environ['CLIENT_SECRET']
CLIENT_SECRET = os.environ['CLIENT_SECRET']
SCOPES = ['https://www.googleapis.com/auth/gmail.compose', 'https://www.googleapis.com/auth/calendar']
APPLICATION_NAME='Bethany Food Bank'

# def get_credentials():
#     """Gets valid user credentials from storage.
#
#     If nothing has been stored, or if the stored credentials are invalid,
#     the OAuth2 flow is completed to obtain the new credentials.
#
#     Returns:
#         Credentials, the obtained credential.
#     """
#     home_dir = os.path.expanduser('~')
#     credential_dir = os.path.join(home_dir, '.credentials')
#     if not os.path.exists(credential_dir):
#         os.makedirs(credential_dir)
#     credential_path = os.path.join(credential_dir,
#                                    'google_oauth_python')
#
#     store = Storage(credential_path)
#     credentials = store.get()
#     if not credentials or credentials.invalid:
#         flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
#         flow.user_agent = APPLICATION_NAME
#         if flags:
#             credentials = tools.run_flow(flow, store, flags)
#         else: # Needed only for compatibility with Python 2.6
#             credentials = tools.run(flow, store)
#         print('Storing credentials to ' + credential_path)
#     return credentials

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/admin_login')
def admin_login():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

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
