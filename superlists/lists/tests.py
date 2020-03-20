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

from lists.models import Item
from lists.views import home_page


class HomePageTest(TestCase):

    # Every single code change is driven by the tests!
    # Don't test constants e.g. HTML as text
    # Unit tests are really about testing logic, flow control, and
    # configuration.
    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')
    # Instead of testing constants we're testing our implementation

    def test_only_saves_items_when_necessary(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)

    def test_can_save_a_POST_request(self):
        response = self.client.post('/', data={'item_text': 'A new list item'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')


class ItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(second_saved_item.text, 'Item the second')

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


#                 Red/Green/Refactor and Traingulation
# The unit-test/code cycle is sometimes taught as Red, Green,
# Refactor:
# * Start by writing a unit test which fails (Red).
# * Write the simplest possible code to get it to pass (Green), even
#   if that means cheating.
# * Refactor to get to better code that makes more sense.

# So what do we do during the Refactor stage? What justifies moving
# from an implementation where we “cheat” to one we’re happy with?
# One methodology is eliminate duplication: if your test uses a magic
# constant (like the “1:” in front of our list item), and your
# application code also uses it, that counts as duplication, so it
# justifies refactoring. Removing the magic constant from the
# application code usually means you have to stop cheating.
# I find that leaves things a little too vague, so I usually like to
# use a second technique, which is called triangulation:
#   If your tests let you get away with writing “cheating” code that
#       you’re not happy with, like returning a magic constant, write
#       another test that forces you to write some better code.
#       That’s what we’re doing when we extend the FT to check that
#       we get a “2:” when inputting a second list item.


#      Unit Tests Versus Integrated Tests, and the Database
# Purists will tell you that a “real” unit test should never touch
# the database, and that the test I’ve just written should be more
# properly called an integrated test, because it doesn’t only test
# our code, but also relies on an external system—that is, a database.

# It’s OK to ignore this distinction for now—we have two types of
# test, the high-level functional tests which test the application
# from the user’s point of view, and these lower-level tests which
# test it from the programmer’s point of view.
