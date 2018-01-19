import httplib2
import os
import oauth2client
from oauth2client import client, tools
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from apiclient import errors, discovery
import mimetypes
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase

from app.oauth_helpers import *

import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


def SendMessage(sender, to, subject, msgHtml, msgPlain, attachmentFile=None):

    credentials = google.oauth2.credentials.Credentials(**session['credentials'])
    service = googleapiclient.discovery.build('gmail', 'v1', credentials=credentials)

    if 'user' in session and session['user'] == 'admin':
        message1 = CreateMessageHtml(sender, to, subject, msgHtml, msgPlain)
        result = SendMessageInternal(service, "me", message1)
        return result
    else:
        redirect(url_for('admin_login'))

def SendMessageInternal(service, user_id, message):
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        print('Message Id: %s' % message['id'])
        return message
    except errors.HttpError as error:
        print('An error occurred: %s' % error)
        return "Error"
    return "OK"

def CreateMessageHtml(sender, to, subject, msgHtml, msgPlain):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = to
    msg.attach(MIMEText(msgPlain, 'plain'))
    msg.attach(MIMEText(msgHtml, 'html'))
    return {'raw': base64.urlsafe_b64encode(msg.as_string().encode()).decode('ascii')}
