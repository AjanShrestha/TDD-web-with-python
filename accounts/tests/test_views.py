from unittest.mock import patch, call
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
        self.assertEqual(from_email, 'playcocwidraka@gmail.com')
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
        expected_url = f'http://testserver/accounts/login?token={token.uid}'
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertIn(expected_url, body)


@patch('accounts.views.auth')  # 1
class LoginViewTest(TestCase):

    def test_redirects_to_home_page(self, mock_auth):  # 2
        response = self.client.get('/accounts/login?token=abcd123')
        self.assertRedirects(response, '/')

    # 2
    def test_calls_authenticate_with_uid_from_get_request(self, mock_auth):
        self.client.get('/accounts/login?token=abcd123')
        self.assertEqual(
            mock_auth.authenticate.call_args,  # 3
            call(uid='abcd123')  # 4
        )

        # 1. We expect to be using the django.contrib.auth module in
        #   views.py, and we mock it out here. Note that this time,
        #   we’re not mocking out a function, we’re mocking out a
        #   whole module, and thus implicitly mocking out all the
        #   functions (and any other objects) that module contains.

        # 2. As usual, the mocked object is injected into our test
        #   method.

        # 3. This time, we’ve mocked out a module rather than a
        #   function. So we examine the call_args not of the
        #   mock_auth module, but of the mock_auth.authenticate
        #   function. Because all the attributes of a mock are more
        #   mocks, that’s a mock too. You can start to see why Mock
        #   objects are so convenient, compared to trying to build
        #   your own.

        # 4. Now, instead of “unpacking” the call args, we use the
        #   call function for a neater way of saying what it should
        #   have been called with-- that is, the token from the GET
        #   request.

    def test_calls_auth_login_with_user_if_there_is_one(self, mock_auth):  # 3
        response = self.client.get('/accounts/login?token=abcd123')
        self.assertEqual(
            mock_auth.login.call_args,  # 2
            call(
                response.wsgi_request,
                mock_auth.authenticate.return_value
            )  # 3
        )

        # 1. We mock the contrib.auth module again.

        # 2. This time we examine the call args for the auth.login
        #   function.

        # 3. We check that it’s called with the request object that
        #   the view sees, and the “user” object that the
        #   authenticate function returns. Because authenticate is
        #   also mocked out, we can use its special “return_value”
        #   attribute.

    def test_does_not_login_if_user_is_not_authenticated(self, mock_auth):
        mock_auth.authenticate.return_value = None  # 4
        self.client.get('/accounts/login?token=abcd123')
        self.assertEqual(mock_auth.login.called, False)  # 5

    # 1. We move the patch to the class level...
    # 2. which means we get an extra argument injected into our first
    #   test method...
    # 3. And we can remove the decorators from all the other tests.
    # 4. In our new test, we explicitly set the return_value on the
    #   auth.authenticate mock, before we call the self.client.get.
    # 5. We assert that, if authenticate returns None, we should not
    #   call auth.login at all.


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

#   An Alternative Reason to Use Mocks: Reducing Duplication
# One good justification for using mocks is when they will reduce
# duplication between tests. It’s one way of avoiding combinatorial
# explosion.


#               On Mock call_args
# The call_args property on a mock represents the positional and
# keyword arguments that the mock was called with. It’s a special
# “call” object type, which is essentially a tuple of
# (positional_args, keyword_args). positional_args is itself a tuple,
# consisting of the set of positional arguments. keyword_args is a
# dictionary.

# >>> from unittest.mock import Mock, call
# >>> m = Mock()
# >>> m(42, 43, 'positional arg 3', key='val', thing=666)
#   <Mock name='mock()' id='139909729163528'>
# >>> m.call_args
#   call(42, 43, 'positional arg 3', key='val', thing=666)
# >>> m.call_args == ((42, 43, 'positional arg 3'), {'key': 'val',
# 'thing': 666})
#   True
# >>> m.call_args == call(42, 43, 'positional arg 3', key='val',
# thing=666)
#   True

# So in our test, we could have done this instead:

    # self.assertEqual(
    #     mock_auth.authenticate.call_args,
    #     ((,), {'uid': 'abcd123'})
    # )

# or this
    # args, kwargs = mock_auth.authenticate.call_args
    # self.assertEqual(args, (,))
    # self.assertEqual(kwargs, {'uid': 'abcd123')

# But you can see how using the call helper is nicer.
