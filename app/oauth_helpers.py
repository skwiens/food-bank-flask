from flask import redirect, request, url_for, session
from app import app

import os
import tempfile
import simplejson as json

import google_auth_oauthlib.flow
import google.oauth2.credentials
import googleapiclient.discovery

# CLIENT_SECRET_FILE = os.environ['CLIENT_SECRET_FILE']
CLIENT_SECRET_FILE = json.loads(os.environ['CLIENT_SECRET_FILE'])

SCOPES = ['https://www.googleapis.com/auth/gmail.compose', 'https://www.googleapis.com/auth/calendar']
APPLICATION_NAME='Bethany Food Bank'
ADMIN_EMAIL = os.environ['ADMIN_EMAIL']

def create_secret_file():
    tmpdir = tempfile.mkdtemp()
    filename = 'client_secret.json'

    path = os.path.join(tmpdir, filename)
    print(path)
    try:
        with open(path, "w") as tmp:
            tmp.write(CLIENT_SECRET_FILE)
            os.environ["CLIENT_SECRET_FILE_PATH"] = path
            print('path is being created!')
            print(path)
    except IOError as e:
        print('IOError')
    else:
        CLIENT_SECRET_FILE_PATH = None
        os.remove(path)
    # finally:
    #     # os.umask(saved_umask)
    #     os.rmdir(tmp)

    return CLIENT_SECRET_FILE_PATH

# def create_file():
#     if os.path.exists('client_secret.json'):
#         # print(os.path('client_secret.json'))
#         f = 'client_secret.json'
#     else:
#         # f = file("client_secret.json", "w")
#         f = open('client_secret.json', 'w')
#         with open('client_secret.json', 'w') as outfile:
#             json.dump(CLIENT_SECRET_FILE, outfile)

def credentials_to_dict(credentials):
  return {'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': credentials.scopes}

@app.route('/authorize')
def authorize():
    # create_file()
    # CLIENT_SECRET_FILE_PATH = os.environ['CLIENT_SECRET_FILE_PATH']


    # flow =google_auth_oauthlib.flow.Flow.from_client_secrets_file(CLIENT_SECRET_FILE, scopes=SCOPES)
    # flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(CLIENT_SECRET_FILE_PATH, scopes=SCOPES)
    # flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(CLIENT_SECRET_FILE, scopes=SCOPES)

    flow=google_auth_oauthlib.flow.Flow.from_client_config(client_config=CLIENT_SECRET_FILE, scopes=SCOPES)



    flow.redirect_uri = url_for('oauth2callback', _external=True)

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true')

    session['state'] = state

    return redirect(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
    # CLIENT_SECRET_FILE_PATH = create_secret_file()
    # CLIENT_SECRET_FILE_PATH = os.environ['CLIENT_SECRET_FILE_PATH']
    state = session['state']

    # flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(CLIENT_SECRET_FILE, scopes=SCOPES, state=state)
    # flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(CLIENT_SECRET_FILE_PATH, scopes=SCOPES, state=state)
    # flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file('client_secret.json', scopes=SCOPES, state=state)

    flow=google_auth_oauthlib.flow.Flow.from_client_config(client_config=CLIENT_SECRET_FILE, scopes=SCOPES)

    flow.redirect_uri = url_for('oauth2callback', _external=True)

    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    session['credentials'] = credentials_to_dict(credentials)

    return redirect(url_for('admin_login'))
