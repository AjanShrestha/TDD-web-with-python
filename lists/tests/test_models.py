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

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.test import TestCase

from lists.models import Item, List

User = get_user_model()


class ItemModelTest(TestCase):

    def test_default_text(self):
        item = Item()
        self.assertEqual(item.text, '')

    def test_item_is_related_to_list(self):
        list_ = List.objects.create()
        item = Item()
        item.list = list_
        item.save()
        self.assertIn(item, list_.item_set.all())

    def test_cannot_save_empty_list_items(self):
        list_ = List.objects.create()
        item = Item(list=list_, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_duplicate_items_are_invalid(self):
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='foo')
        with self.assertRaises(ValidationError):
            item = Item(list=list_, text='foo')
            item.full_clean()

    def test_CAN_save_same_item_to_different_lists(self):
        list1 = List.objects.create()
        list2 = List.objects.create()
        Item.objects.create(list=list1, text='bla')
        item = Item(list=list2, text='bla')
        item.full_clean()  # should not raise

    def test_list_ordering(self):
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text='item 1')
        item2 = Item.objects.create(list=list1, text='item 2')
        item3 = Item.objects.create(list=list1, text='item 3')
        self.assertEqual(
            list(Item.objects.all()),
            [item1, item2, item3]
        )

    def test_string_representation(self):
        item = Item(text='some text')
        self.assertEqual(str(item), 'some text')


class ListModelTest(TestCase):
    def test_get_absolute_url(self):
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), f'/lists/{list_.id}/')

    def test_list_name_is_first_item_text(self):
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='first item')
        Item.objects.create(list=list_, text='second item')
        self.assertEqual(list_.name, 'first item')

    def test_create_new_creates_list_and_first_item(self):
        List.create_new(first_item_text='new item text')
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'new item text')
        new_list = List.objects.first()
        self.assertEqual(new_item.list, new_list)

    def test_create_new_optionally_saves_owner(self):
        user = User.objects.create()
        new_list = List.create_new(first_item_text='new item text', owner=user)
        self.assertEqual(new_list.owner, user)

    def test_create_returns_new_list_object(self):
        returned = List.create_new(first_item_text='new item text')
        new_list = List.objects.first()
        self.assertEqual(returned, new_list)

    def test_can_share_with_another_user(self):
        list_ = List.objects.create()
        user = User.objects.create(email='a@b.com')
        list_.shared_with.add('a@b.com')
        list_in_db = List.objects.get(id=list_.id)
        self.assertIn(user, list_in_db.shared_with.all())

    def test_lists_can_have_owners(self):
        List(owner=User())  # should not raise

    def test_lists_owner_is_optional(self):
        List().full_clean()  # should not raise


#                Useful Commands and Concepts
# Running the Django dev server
#   python manage.py runserver
# Running the functional tests
#   python functional_tests.py
# Running the unit tests
#   python manage.py test

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


#                   In Memory
# Use in-memory (unsaved) model objects in your tests whenever you
# can; it makes your tests faster.
