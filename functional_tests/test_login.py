from apiclient import errors
from django.core import mail
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from selenium.webdriver.common.keys import Keys
import base64
import email
import os.path
import pickle


import re

from .base import FunctionalTest

SUBJECT = 'Your login link for Superlists'


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


class GmailInbox:
    def __init__(self):
        self._service = GmailInbox.get_gmail_api_service()
        self._user_id = 'me'

    @staticmethod
    def get_gmail_api_service():
        """Shows basic usage of the Gmail API.
        Lists the user's Gmail labels.
        """
        creds = None
        # The file token.pickle stores the user's access and refresh
        # tokens, and is created automatically when the authorization
        # flow completes for the first time.
        if os.path.exists('functional_tests/token.pickle'):
            with open('functional_tests/token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'functional_tests/credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('functional_tests/token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('gmail', 'v1', credentials=creds)
        return service

    @staticmethod
    def get_email_properties(message):
        headers = {
            header['name']: header['value']
            for header in message['payload']['headers']
        }
        return {
            'email_to': headers['To'],
            'subject': headers['Subject'],
            'body': message['snippet']
        }

    def user(self, email):
        self._email = email

    def stat(self):
        try:
            all_messages = self._service.users().messages().list(
                userId=self._user_id).execute()['messages']
            self._messages = all_messages['messages']
            return len(self._messages), self._messages
        except Exception as error:
            print('An error occurred: %s' % error)

    def retr(self, index):
        return self._messages[index]['id']

    def props(self, msg_id):
        try:
            message = self._service.users().messages().get(
                userId=self._user_id, id=msg_id, format='metadata').execute()
        except Exception as error:
            print('An error occurred: %s' % error)
        email_props = GmailInbox.get_email_properties(message)
        return email_props

    def delete(self, msg_id):
        try:
            self._service.users().messages().delete(
                userId=self._user_id, id=msg_id).execute()
            print('Message with id: %s deleted successfully.' % msg_id)
        except errors.HttpError as error:
            print('An error occurred: %s' % error)


class LoginTest(FunctionalTest):

    def wait_for_email(self, test_email, subject):
        if not self.staging_server:
            email = mail.outbox[0]
            self.assertIn(test_email, email.to)
            self.assertEqual(email.subject, subject)
            return email.body

        email_id = None
        start = time.time()
        inbox = GmailInbox()
        try:
            inbox.user(test_email)
            while time.time() - start < 60:
                # get 10 newest messages
                count, _ = inbox.stat()
                for i in reversed(range(max(0, count - 10), count)):
                    print('getting msg', i)
                    msg_id = inbox.retr(i)
                    email_props = inbox.props(msg_id)
                    if subject in email_props['subject'] and test_email in email_props['email_to']:
                        email_id = msg_id
                        body = email_props['body']
                        return body
                time.sleep(5)
        finally:
            if email_id:
                inbox.delete(email_id)
            inbox.quit()

    def test_can_get_email_link_to_log_in(self):
        # Edith goes to the awesome superlists site and notices a
        # "Log in" section in the navbar for the first time
        # It's telling her to enter her email address, so she does
        if self.staging_server:
            test_email = 'playcocwidraka@gmail.com'
        else:
            test_email = 'edith@example.com'
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_name('email').send_keys(test_email)
        self.browser.find_element_by_name('email').send_keys(
            Keys.ENTER
        )

        # A message appears telling her an email has been sent
        self.wait_for(lambda: self.assertIn(
            'Check your email',
            self.browser.find_element_by_tag_name('body').text
        ))

        # She checks her email and finds a message
        body = self.wait_for_email(test_email, SUBJECT)

        # It has a url link in it
        self.assertIn('Use this link to log in', body)
        url_search = re.search(r'http://.+/.+$', body)
        if not url_search:
            self.fail(f'Could not find url in email body:\n{body}')
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # she clicks it
        self.browser.get(url)

        # she is logged in!
        self.wait_to_be_logged_in(email=test_email)

        # Now she logs out
        self.browser.find_element_by_link_text('Log out').click()

        # She is logged out
        self.wait_to_be_logged_out(email=test_email)
