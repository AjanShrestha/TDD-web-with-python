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
from django.http import HttpRequest
from django.test import TestCase
from django.urls import resolve
from django.utils.html import escape
from unittest.mock import patch, Mock
import unittest

from lists.forms import (
    DUPLICATE_ITEM_ERROR, EMPTY_ITEM_ERROR,
    ExistingListItemForm, ItemForm
)
from lists.models import Item, List
from lists.views import new_list

User = get_user_model()


class HomePageTest(TestCase):

    # Every single code change is driven by the tests!
    # Don't test constants e.g. HTML as text
    # Unit tests are really about testing logic, flow control, and
    # configuration.
    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')
    # Instead of testing constants we're testing our implementation

    def test_home_page_uses_item_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)


class NewListViewIntegratedTest(TestCase):

    def test_can_save_a_POST_request(self):
        self.client.post('/lists/new', data={'text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_for_invalid_input_doesnt_save_but_shows_errors(self):
        response = self.client.post(
            '/lists/new', data={'text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_list_owner_is_saved_if_user_is_authenticated(self):
        user = User.objects.create(email='a@b.com')
        self.client.force_login(user)
        self.client.post('/lists/new', data={'text': 'new item'})
        list_ = List.objects.first()
        self.assertEqual(list_.owner, user)


@patch('lists.views.NewListForm')
class NewListViewUnitTest(unittest.TestCase):

    def setUp(self):
        self.request = HttpRequest()
        self.request.POST['text'] = 'new list item'
        self.request.user = Mock()

    def test_passess_POST_data_to_NewListForm(self, mockNewListForm):
        new_list(self.request)
        mockNewListForm.assert_called_once_with(data=self.request.POST)

    def test_saves_form_with_owner_if_form_valid(self, mockNewListForm):
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = True
        new_list(self.request)
        mock_form.save.assert_called_once_with(owner=self.request.user)

    def test_does_not_save_if_form_invalid(self, mockNewListForm):
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = False
        new_list(self.request)
        self.assertFalse(mock_form.save.called)

    @patch('lists.views.redirect')  # 1
    # 2
    def test_redirects_to_form_returned_object_if_form_valid(self, mock_redirect, mockNewListForm):
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = True  # 3

        response = new_list(self.request)

        self.assertEqual(response, mock_redirect.return_value)  # 4
        mock_redirect.assert_called_once_with(mock_form.save.return_value)  # 5

        # 1. We mock out the redirect function, this time at the
        #   method level.
        # 2. patch decorators are applied innermost first, so the new
        #   mock is injected to our method as before the
        #   mockNewListForm.
        # 3. We specify that we’re testing the case where the form is
        #   valid.
        # 4. We check that the response from the view is the result
        #   of the redirect function.
        # 5. And we check that the redirect function was called with
        #   the object that the form returns on save.

    # When doing Outside-In TDD with isolated tests, you need to keep
    # track of each test’s implicit assumptions about the contract
    # which the next layer should implement, and remember to test
    # each of those in turn later. You could use our scratchpad for
    # this, or create a placeholder test with a self.fail.

    @patch('lists.views.render')
    def test_redirects_to_form_returned_object_if_form_invalid(self, mock_render, mockNewListForm):
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = False

        response = new_list(self.request)

        self.assertEqual(response, mock_render.return_value)
        mock_render.assert_called_once_with(
            self.request, 'home.html', {'form': mock_form})


class ListViewTest(TestCase):

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'list.html')

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'], correct_list)
    # response.context represents the context we're going to pass into
    # the render function -- the Django Client puts it on the
    # response object for us, to help with testing

    def test_displays_item_form(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertIsInstance(response.context['form'], ExistingListItemForm)
        self.assertContains(response, 'name="text"')

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='other list item 1', list=other_list)
        Item.objects.create(text='other list item 2', list=other_list)

        response = self.client.get(f'/lists/{correct_list.id}/')

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other list item 1')
        self.assertNotContains(response, 'other list item 2')

    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            f'/lists/{correct_list.id}/',
            data={'text': 'A new item for an existing list'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_POST_redirets_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            f'/lists/{correct_list.id}/',
            data={'text': 'A new item for an existing list'}
        )

        self.assertRedirects(response, f'/lists/{correct_list.id}/')

    def post_invalid_input(self):
        list_ = List.objects.create()
        return self.client.post(
            f'/lists/{list_.id}/',
            data={'text': ''}
        )

    def test_for_invalid_input_nothing_saved_to_db(self):
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)

    def test_for_invalid_input_renders_list_template(self):
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')

    def test_for_invalid_input_passes_from_to_template(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], ExistingListItemForm)

    def test_for_invalid_input_shows_error_on_page(self):
        response = self.post_invalid_input()
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    # We’ve seen this several times now. It often feels more natural
    # to write view tests as a single, monolithic block of
    # assertions—the view should do this and this and this, then
    # return that with this. But breaking things out into multiple
    # tests is definitely worth‐while; as we saw in previous
    # chapters, it helps you isolate the exact problem you may have,
    # when you later come and change your code and accidentally
    # introduce a bug. Helper methods are one of the tools that lower
    # the psychological barrier.

    def test_duplicate_item_validation_errors_end_up_on_lists_page(self):
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text='textey')
        response = self.client.post(
            f'/lists/{list1.id}/',
            data={'text': 'textey'}
        )

        expected_error = escape(DUPLICATE_ITEM_ERROR)
        self.assertContains(response, expected_error)
        self.assertTemplateUsed(response, 'list.html')
        self.assertEqual(Item.objects.all().count(), 1)


class MyListsTest(TestCase):

    def test_my_lists_url_renders_my_lists_template(self):
        User.objects.create(email='a@b.com')
        response = self.client.get('/lists/users/a@b.com/')
        self.assertTemplateUsed(response, 'my_lists.html')

    def test_passes_correct_owner_to_template(self):
        User.objects.create(email='wrong@owner.com')
        correct_user = User.objects.create(email='a@b.com')
        response = self.client.get('/lists/users/a@b.com/')
        self.assertEqual(response.context['owner'], correct_user)


class ShareListTest(TestCase):

    def test_sharing_a_list_via_post(self):
        sharee = User.objects.create(email='share.with@me.com')
        list_ = List.objects.create()
        self.client.post(
            f'/lists/{list_.id}/share',
            {'sharee': 'share.with@me.com'}
        )
        self.assertIn(sharee, list_.shared_with.all())

    def test_redirects_after_POST(self):
        sharee = User.objects.create(email='share,with@me.com')
        list_ = List.objects.create()
        response = self.client.post(
            f'/lists/{list_.id}/share',
            {'sharee': 'share.with@me.com'}
        )
        self.assertRedirects(response, list_.get_absolute_url())


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


#                   What to Test in Views
# class ListViewTest(TestCase):
#   def test_uses_list_template(self):
#       response = self.client.get(f'/lists/{list_.id}/')        [1]
#       self.assertTemplateUsed(response, 'list.html')           [2]
#   def test_passes_correct_list_to_template(self):
#       self.assertEqual(response.context['list'], correct_list) [3]
#   def test_displays_item_form(self):
#       self.assertIsInstance(response.context['form'],          [4]
#           ExistingListItemForm)
#       self.assertContains(response, 'name="text"')
#   def test_displays_only_items_for_that_list(self):
#       self.assertContains(response, 'itemey 1')                [5]
#       self.assertContains(response, 'itemey 2')                [5]
#       self.assertNotContains(response, 'other list item 1')    [5]
#   def test_can_save_a_POST_request_to_an_existing_list(self):
#       self.assertEqual(Item.objects.count(), 1)                [6]
#       self.assertEqual(new_item.text, 'A new item for an existing
#           list')                                               [6]
#   def test_POST_redirects_to_list_view(self):
#       self.assertRedirects(response, f'/lists/{correct_list.id}/')
#                                                                [6]
#   def test_for_invalid_input_nothing_saved_to_db(self):
#       self.assertEqual(Item.objects.count(), 0)                [6]
#   def test_for_invalid_input_renders_list_template(self):
#       self.assertEqual(response.status_code, 200)
#       self.assertTemplateUsed(response, 'list.html')           [6]
#   def test_for_invalid_input_passes_form_to_template(self):
#       self.assertIsInstance(response.context['form'],
#           ExistingListItemForm)                                [7]
#   def test_for_invalid_input_shows_error_on_page(self):
#       self.assertContains(response, escape(EMPTY_ITEM_ERROR))  [7]
#   def test_duplicate_item_validation_errors_end_up_on_lists_page
#       (self):
#       self.assertContains(response, expected_error)
#       self.assertTemplateUsed(response, 'list.html')
#       self.assertEqual(Item.objects.all().count(), 1)

# 1. Use the Django Test Client.
# 2. Check the template used. Then, check each item in the template
#       context.
# 3. Check that any objects are the right ones, or querysets have the
#       correct items.
# 4. Check that any forms are of the correct class.
# 5. Think about testing template logic: any for or if might deserve
#       a minimal test.
# 6. For POST requests, make sure you test both the valid case and
#       the invalid case.
# 7. Optionally, sanity-check that your form is rendered, and its
#       errors are displayed.


#               Thinking in Terms of Collaborators
# In order to rewrite our tests to be fully isolated, we need to
# throw out our old way of thinking about the tests in terms of the
# “real” effects of the view on things like the database, and instead
# think of it in terms of the objects it collaborates with, and how
# it interacts with them.

# In the new world, the view’s main collaborator will be a form
# object, so we mock that out in order to be able to fully control
# it, and in order to be able to define, by wishful thinking, the way
# we want our form to work:


# Here’s an important lesson to learn about test isolation: it might
# help you to drive out good design for individual layers, but it
# won’t automatically verify the integration between your layers.


#       Thinking of Interactions Between Layers as “Contracts”
# Ultimately, even if we had been writing nothing but isolated unit
# tests, our functional tests would have picked up this particular
# slip-up. But ideally we’d want our feedback cycle to be
# quicker—functional tests may take a couple of minutes to run, or
# even a few hours once your app starts to grow. Is there any way to
# avoid this sort of problem before it happens?

# Methodologically, the way to do it is to think about the
# interaction between your layers in terms of contracts. Whenever
# we mock out the behaviour of one layer, we have to make a mental
# note that there is now an implicit contract between the layers, and
# that a mock on one layer should probably translate into a test at
# the layer below.
