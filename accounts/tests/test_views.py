from unittest.mock import patch
from django.test import TestCase
from unittest.mock import patch

import accounts.views
from accounts.models import Token


class SendLoginEmailViewTest(TestCase):

    def test_redirects_to_home_page(self):
        response = self.client.post(
            '/accounts/send_login_email',
            data={'email': 'edith@example.com'}
        )
        self.assertRedirects(response, '/')

    def test_adds_success_message(self):
        response = self.client.post(
            '/accounts/send_login_email',
            data={'email': 'edith@example.com'},
            follow=True
        )

        message = list(response.context['messages'])[0]
        self.assertEqual(
            message.message,
            "Check your email, we've sent you a link you can use to log in."
        )
        self.assertEqual(message.tags, "success")

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

    def test_creates_token_associated_with_email(self):
        self.client.post(
            '/accounts/send_login_email',
            data={'email': 'edith@example.com'}
        )
        token = Token.objects.first()
        self.assertEqual(token.email, 'edith@example.com')

    @patch('accounts.views.send_mail')
    def test_sends_link_to_login_using_token_uid(self, mock_send_mail):
        self.client.post(
            '/accounts/send_login_email',
            data={'email': 'edith@example.com'}
        )
        token = Token.objects.first()
        expected_url = f'http://testserver/accounts/login?token={token.id}'
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertIn(expected_url, body)


class LoginViewTest(TestCase):

    def test_redirects_to_home_page(self):
        response = self.client.get('/accounts/login?token=abcd123')
        self.assertRedirects(response, '/')


#   Mocks Can Leave You Tightly Coupled to the Implementation
# This sidebar is an intermediate-level testing tip. If it goes over
# your head the first time around, come back and take another look
# when you’ve finished this chapter and Chapter 23.

# I said testing messages is a bit contorted; it took me several goes
# to get it right. In fact, at work, we gave up on testing them like
# this and decided to just use mocks. Let’s see what that would look
# like in this case:

# accounts/tests/test_views.py
# @patch('accounts.views.messages')
# def test_adds_success_message_with_mocks(self, mock_messages):
#     response = self.client.post(
#         '/accounts/send_login_email',
#         data={'email': 'edith@example.com'}
#     )
#     expected = "Check your email, we've sent you a link you can use to log in."
#     self.assertEqual(
#         mock_messages.success.call_args,
#         call(response.wsgi_request, expected),
#     )

# We mock out the messages module, and check that messages.success
# was called with the right args: the original request, and the
# message we want.
# And you could get it passing by using the exact same code as
# earlier. Here’s the problem though: the messages framework gives
# you more than one way to achieve the same result. I could write the
# code like this:

    # messages.add_message(
    #     request,
    #     messages.SUCCESS,
    #     "Check your email, we've sent you a link you can use to log in."
    # )

# And the original, nonmocky test would still pass. But our mocky
# test will fail, because we’re no longer calling messages.success,
# we’re calling messages.add_message. Even though the end result is
# the same and our code is “correct, ” the test is broken.

# **
# This is what people mean when they say that using mocks can leave
# you “tightly coupled with the implementation”. We usually say it’s
# better to test behaviour, not implementation details test what
# happens, not how you do it. Mocks often end up erring too much on
# the side of the “how” rather than the “what”.
