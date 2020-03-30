from django.conf import settings

from .base import FunctionalTest
from .server_tools import create_session_on_server
from .management.commands.create_session import create_pre_authenticated_session


class MyListsTest(FunctionalTest):

    def create_pre_authenticated_session(self, email):
        # 1
        if self.staging_server:
            session_key = create_session_on_server(self.staging_server, email)
        else:
            session_key = create_pre_authenticated_session(email)
        # to set a cookie we need to first visit the domain.
        # 404 pages load the quickest!
        self.browser.get(self.live_server_url + "/404_no_such_url/")
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session_key,  # 2
            path='/',
        ))
        # 1. We create a session object in the database. The session
        #   key is the primary key of the user object (which is
        #   actually the user’s email address).
        # 2. We then add a cookie to the browser that matches the
        #   session on the server—on our next visit to the site, the
        #   server should recognise us as a logged-in user.

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        email = 'edith@example.com'
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_out(email)

        # Edith is a logged-in user
        self.create_pre_authenticated_session(email)
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_in(email)


#       JSON test Fixtures Considered Harmful

# When we pre-populate the database with test data, as we’ve done
# here with the User object and its associated Session object, what
# we’re doing is setting up a “test fixture”.

# Django comes with built-in support for saving database objects as
# JSON (using the manage.py dumpdata), and automatically loading them
# in your test runs using the fixtures class attribute on TestCase.

# More and more people are starting to say: don’t use JSON fixtures.
# They’re a nightmare to maintain when your model changes. Plus it’s
# difficult for the reader to tell which of the many attribute values
# specified in the JSON are critical for the behaviour under test,
# and which are just filler. Finally, even if tests start out sharing
# fixtures, sooner or later one test will want slightly different
# versions of the data, and you end up copying the whole thing around
# to keep them isolated, and again it’s hard to tell what’s relevant
# to the test and what is just happenstance.

# It’s usually much more straightforward to just load the data
# directly using the Django ORM.

# Once you have more than a handful of fields on a model, and/or
# several related models, even using the ORM can be cumbersome. In
# this case, there’s a tool that lots of people swear by called
# factory_boy.
