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

from django.test import TestCase

from lists.models import Item, List


class ListAndItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.list, list_)

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

#   Better Unit Testing Practice: Each Test Should Test One Thing
# Good unit testing practice says that each test should only test one
# thing. The reason is that it makes it easier to track down bugs.
# Having multiple assertions in a test means that, if the test fails
# on an early assertion, you don’t know what the status of the later
# assertions is.


#                   Usefule TD Concepts
# Regression
#   When new code breaks some aspect of the application which used to
#   work.
# Unexpected failure
#   When a test fails in a way we weren’t expecting. This either
#   means that we’ve made a mistake in our tests, or that the tests
#   have helped us find a regression, and we need to fix something in
#   our code.
# Red/Green/Refactor
#   Another way of describing the TDD process. Write a test and see
#   it fail (Red), write some code to get it to pass (Green), then
#   Refactor to improve the implementation.
# Traingulation
#   Adding a test case with a new specific example for some existing
#   code, to justify generalising the implementation (which may be a
#   “cheat” until that point).
# Three strikes and refactor
#   A rule of thumb for when to remove duplication from code. When
#   two pieces of code look very similar, it often pays to wait until
#   you see a third use case, so that you’re more sure about what
#   part of the code really is the common, re-usable part to refactor
#   out.
# The scrathpad to-do list
#   A place to write down things that occur to us as we’re coding, so
#   that we can finish up what we’re doing and come back to them
#   later.


# A second clue is the rule of thumb that, when all the unit tests
# are passing but the functional tests aren’t, it’s often pointing at
# a problem that’s not covered by the unit tests, and in our case,
# that’s often a template problem.


#             Some More TDD Philosophy
# Working State to Working State (aka The Testing Goat vs.
# Refactoring Cat)
#   Our natural urge is often to dive in and fix everything at once...
#   but if we’re not careful, we’ll end up like Refactoring Cat, in a
#   situation with loads of changes to our code and nothing working.
#   The Testing Goat encourages us to take one step at a time, and go
#   from working state to working state.
# Split work out into small, achievable tasks
#   Sometimes this means starting with “boring” work rather than
#   diving straight in with the fun stuff, but you’ll have to trust
#   that YOLO-you in the parallel universe is probably having a bad
#   time, having broken everything, and struggling to get the app
#   working again.
# YAGNI
#   You ain’t gonna need it! Avoid the temptation to write code that
#   you think might be useful, just because it suggests itself at the
#   time. Chances are, you won’t use it, or you won’t have
#   anticipated your future requirements correctly.
