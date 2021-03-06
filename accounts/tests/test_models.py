from django.test import TestCase
from django.contrib import auth

from accounts.models import Token

User = auth.get_user_model()


class UserModelTest(TestCase):

    def test_user_is_valid_with_email_only(self):
        user = User(email='a@b.com')
        user.full_clean()  # should not raise

    def test_email_is_primary_key(self):
        user = User(email='a@b.com')
        self.assertEqual(user.pk, 'a@b.com')

    def test_no_problem_with_auth_login(self):
        user = User.objects.create(email='edith@example.com')
        user.backend = ''
        request = self.client.request().wsgi_request
        auth.login(request, user)  # should not raise
        # We create a request object and a user, and then we pass
        # them into the auth.login function.


class TokenModelTest(TestCase):

    def test_links_user_with_auto_generated_uid(self):
        token1 = Token.objects.create(email='a@b.com')
        token2 = Token.objects.create(email='a@b.com')
        self.assertNotEqual(token1.uid, token2.uid)


# Your tests can be a form of documentation for your code—they
# express what your requirements are of a particular class or
# function. Sometimes, if you forget why you’ve done something a
# particular way, going back and looking at the tests will give you
# the answer. That’s why it’s important to give your tests explicit,
# verbose method names.
