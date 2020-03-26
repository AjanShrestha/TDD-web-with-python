from django.test import TestCase
from unittest.mock import patch

import accounts.views


class SendLoginEmailViewTest(TestCase):

    def test_redirects_to_home_page(self):
        response = self.client.post(
            '/accounts/send_login_email',
            data={'email': 'edith@example.com'}
        )
        self.assertRedirects(response, '/')

    @patch('accounts.views.send_mail')  # 1
    def test_sends_email_to_address_from_post(self, mock_send_mail):  # 2
        self.client.post(
            '/accounts/send_login_email',
            data={'email': 'edith@example.com'}  # 3
        )

        self.assertEqual(mock_send_mail.called, True)  # 4
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args  # 5
        self.assertEqual(subject, 'Your login link for Superlists')
        self.assertEqual(from_email, 'noreply@superlists')
        self.assertEqual(to_list, ['edith@example.com'])

        # 1. The patch decorator takes a dot-notation name of an
        #   object to monkeypatch. That’s the equivalent of manually
        #   replacing the send_mail in accounts.views. The advantage
        #   of the decorator is that, firstly, it automatically
        #   replaces the target with a mock. And secondly, it
        #   automatically puts the original object back at the end!
        #   (Otherwise, the object stays monkeypatched for the rest
        #   of the test run, which might cause problems in other
        #   tests.)

        # 2. patch then injects the mocked object into the test as an
        #   argument to the test method. We can choose whatever name
        #   we want for it, but I usually use a convention of mock_
        #   plus the original name of the object.

        # 3. We call our function under test as usual, but everything
        #   inside this test method has our mock applied to it, so
        #   the view won’t call the real send_mail object; it’ll be
        #   seeing mock_send_mail instead.

        # 4. And we can now make assertions about what happened to
        #   that mock object during the test. We can see it was
        #   called...

        # 5. ...and we can also unpack its various positional and
        #   keyword call arguments, and examine what it was called
        #   with.
