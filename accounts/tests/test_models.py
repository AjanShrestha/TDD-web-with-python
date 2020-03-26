from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserModelTest(TestCase):

    def test_user_is_valid_with_email_only(self):
        user = User(email='a@b.com')
        user.full_clean()  # should not raise

    def test_email_is_primary_key(self):
        user = User(email='a@b.com')
        self.assertEqual(user.pk, 'a@b.com')


# Your tests can be a form of documentation for your code—they
# express what your requirements are of a particular class or
# function. Sometimes, if you forget why you’ve done something a
# particular way, going back and looking at the tests will give you
# the answer. That’s why it’s important to give your tests explicit,
# verbose method names.
