# Unit Test, and How They differ from Functional Tests
# Functional tests test the application from the outside, from the
# point of view of the user.
# Unit tests test the application from the inside, from the point of
# view of the programmer.

# TDD approach workflow for our application
# 1. We start by writing a functional test, describing the new
#   functionality from the user's point of view.
# 2. Once we have a functional test that fails, we start to think
#   about how to write code that can get it to pass (or at least to
#   get past its current failure). We now use one or more unit tests
#   to define how we want our code to behave -- the idea is that each
#   line of production code we write should be tested by (at least)
#   one of our unit tests.
# 3. Once we have a failing unit test, we write the smallest amount
#   of application code we can, just enough to get the unit test to
#   pass. We may iterate between step 2 and 3 a few times, until we
#   think the functional test will get a litle further.
# 4. Now we can rerun our functional tests and see if they pass, or
#   get a little further. That may prompt us to write some new unit
#   tests, and some new code, and so on.

# The functional tests are driving what development we do from a high
# level, while the unit tests drive what we do at a low level.

# Functional tests should help you build an application with the
# right functionality, and guarantee you never accidentally break it.
# Unit tests should help you to write code that's clean and bug free.

# So we want to test two things:
# * Can we resolve the URL for the root of the site("/") to a
#   particular view function we've made?
# * Can we make this view function return some HTML which wll get the
#   functional test to pass?


# On the Merits of Trivial Tests for Trivial Functions
# In the short term it may feel a bit silly to write tests for simple
# functions and constants.
# Rigorous TDD is like a kata in a martial art, the idea is to learn
# the motions in a controlled context, when there is no adversity, so
# that the techniques are part of your muscle memory. The problem
# comes when your application gets complex -- that's when you really
# need your tests. And the danger is that complexity tends to sneak
# up on you, gradually. You may not notice it happening, but quite
# soon you're a boiled frog.
# Two other things in favor of tiny, simple tests for simple
# functions.
# 1. Firstly, if they're really trivial tests, then they won't take
#   you that long to write them. So, stop moaning and just write them
#   already.
# 2. Secondly, it's always good to have a placeholder. Having a test
#   there for a simple function means it's that much less a
#   psychological barrier to overcome when the simple function gets a
#   tiny bit more complex. Because it's had tests from the very
#   beginning, adding a new test each time has felt quite natural,
#   and it's well tested. The alternative involves trying to decide
#   when a function becomes “complicated enough”, which is highly
#   subjective, but worse, because there’s no placeholder, it seems
#   like that much more effort, and you’re tempted each time to put
#   it off a little longer, and pretty soon—frog soup!

from django.http import HttpRequest
from django.urls import resolve
from django.template.loader import render_to_string
from django.test import TestCase

from lists.views import home_page


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)
    # 1. resolve is the function Django uses internally to resolve
    #   URLs and find what view function they should map to.
    # 2. What function is that? It's the view function which will
    #   actually return the HTML we want.
    # Every single code change is driven by the tests!

    # Don't test constants e.g. HTML as text
    # Unit tests are really about testing logic, flow control, and
    # configuration.
    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')
    # Instead of testing constants we're testing our implementation

#                Useful Commands and Concepts
# Running the Django dev server
#   python manage.py runserver
# Running the functional tests
#   python functional_tests.py
# Running the unit tests
#   python manage.py test

# The unit-test/code cycle
# 1. Run the unit tests in the terminal
# 2. Make a minimal code change in the editor
# 3. Repeat!
