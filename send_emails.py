from __future__ import print_function
from googleapiclient.discovery import build
from apiclient import errors
from httplib2 import Http
from email.mime.text import MIMEText
import base64
from google.oauth2 import service_account
import pickle
import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


def create_message(sender, to, subject, message_text):
    """Create a message for an email.
    Args:
        sender: Email address of the sender.
        to: Email address of the receiver.
        subject: The subject of the email message.
        message_text: The text of the email message.
    Returns:
        An object containing a base64url encoded email object.
    """
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}

def send_message(service, user_id, message):
    """Send an email message.
    Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        message: Message to be sent.
    Returns:
        Sent Message.
    """
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        print('Message Id: %s' % message['id'])
        return message
    except errors.HttpError as error:
        print('An error occurred: %s' % error)

def service_account_login():
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']

    """Shows basic usage of the Gmail API.
        Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    return service

def gen_emails(directory):
    email_contents = []
    path, dirs, files = next(os.walk(directory))

    for file in files:
        if file == 'SUMMARY.txt':
            continue

        f = open(os.path.join(directory,file),'r')
        lines = f.readlines()
        f.close()

        email_contents.append((lines[0][:-1],''.join(lines[1:])))

    return email_contents


service = service_account_login()

EMAIL_FROM = 'sgolden2@hawk.iit.edu'
EMAIL_SUBJECT = 'Your CS340 MP2 Report'

emails = gen_emails(os.path.abspath('G:/My Drive/School/TACS340/2022/mp2/mp2reports'))
print([x[0] for x in emails])

for email in emails:
    EMAIL_CONTENT = ''
    EMAIL_TO = f"{email[0]}@hawk.iit.edu"
    #EMAIL_TO = "samgolden00@gmail.com"
    EMAIL_CONTENT += "Hello!\n\nYour grade report for MP2 in CS340 is below:"
    EMAIL_CONTENT += '\n\n' + email[0] + '\n' + email[1]
    EMAIL_CONTENT += "\n\nIf you think I have made a mistake (which is very possible), or you have any questions, please respond to this email or shoot me a message on Discord. Please also note that this grade does not take into account late days. If you have a score listed here, but a zero listed on Blackboard, it probably means that you submitted more than 7 days after the submission deadline. Please ask me if you'd like to know how many late days you have remaining.\n\nThanks,\nSam\n\n(p.s. this is an automated message, but it is from my real email address, so you can still respond to it)"
    message = create_message(EMAIL_FROM, EMAIL_TO, EMAIL_SUBJECT, EMAIL_CONTENT)
    sent = send_message(service,'me', message)
    print(sent)

