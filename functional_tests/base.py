#                   Terminology:
# Functional Test == Acceptance Test == End-to-End Test
# These kinds of tests look at how the whole application functions,
# from the oustide. Another term is black box test, because the test
# doesn't know anything about the internals of the system under the
# test.
# Let us see how the application functions from the user's point of
# view. This means that an FT can be a sort of specification for your
# application. It tends to track User Story - follows how the user
# might work with a particular feature and how the app should respond
# to them.


from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import os
import time


MAX_WAIT = 10


def wait(fn):  # 1
    def modified_fn(*args, **kwargs):  # 3 # 6
        start_time = time.time()
        while True:  # 4
            try:
                return fn(*args, **kwargs)  # 5 # 7
            except (AssertionError, WebDriverException) as e:  # 4
                if (time.time() - start_time) > MAX_WAIT:
                    raise e
                time.sleep(0.5)
    return modified_fn  # 2
    # 1. A decorator is a way of modifying a function; it takes a
    #   function as an argument...
    # 2. and returns another function as the modified (or “decorated”
    #   ) version.
    # 3. Here’s where we create our modified function.
    # 4. And here’s our familiar loop, which will keep going,
    #   catching the usual exceptions, until our timeout expires.
    # 5. And as always, we call our function and return immediately
    #   if there are no exceptions.
    # 6. Using *args and **kwargs, we specify that modified_fn may
    #   take any arbitrary positional and keyword arguments.
    # 7. As we’ve captured them in the function definition, we make
    #   sure to pass those same arguments to fn when we actually call
    #   it.


class FunctionalTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server

    def tearDown(self):
        # The only exception tearDown doesn't run is if an exception
        # inside setUp
        self.browser.quit()

    @wait
    def wait_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    @wait
    def wait_for(self, fn):
        return fn()

    def get_item_input_box(self):
        return self.browser.find_element_by_id('id_text')

    @wait
    def wait_to_be_logged_in(self, email):
        self.browser.find_element_by_link_text('Log out')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn(email, navbar.text)

    @wait
    def wait_to_be_logged_out(self, email):
        self.browser.find_element_by_name('email')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertNotIn(email, navbar.text)


# First functional test (FT)
# What it's doing
#   Starting a Selenium "webdriver" to pop up a real Firefix browser
#       window
#   Using it to open up a web page which we're expecting to be served
#       from the local PC
#   Checking (making a test assertion) that the page has the word
#       "Django" in its title

#                            Useful TDD Concepts
# User Story
#   A description of how the application will work from the point of
#      view of the user.
# Expected failure
#   When a test fails in the way that we expected it to.


#               Testing "Best Practices"
# Ensuring test isolation and managing global state
#   Different tests shouldn’t affect one another. This means we need
#   to reset any per‐ manent state at the end of each test. Django’s
#   test runner helps us do this by creating a test database, which
#   it wipes clean in between each test.
# Avoid "voodoo" sleeps
#   Whenever we need to wait for something to load, it’s always
#   tempting to throw in a quick-and-dirty time.sleep. But the
#   problem is that the length of time we wait is always a bit of a
#   shot in the dark, either too short and vulnerable to spurious
#   failures, or too long and it’ll slow down our test runs. Prefer a
#   retry loop that polls our app and moves on as soon as possible.
# Dont' rely on Selenium's implicit waits
#   Selenium does theoretically do some “implicit” waits, but the
#   implementation varies between browsers, and at the time of
#   writing was highly unreliable in the Selenium 3 Firefox driver.
#   “Explicit is better than implict”, as the Zen of Python says, so
#   prefer explicit waits.


#               On Testing Design and Layout
# The short answer is: you shouldn’t write tests for design and
# layout per se. It’s too much like testing a constant, and the tests
# you write are often brittle.

# With that said, the implementation of design and layout involves
# something quite tricky: CSS and static files. As a result, it is
# valuable to have some kind of minimal “smoke test” which checks
# that your static files and CSS are working. It can help pick up
# problems when you deploy your code to production.

# Similarly, if a particular piece of styling required a lot of
# client-side JavaScript code to get it to work (dynamic resizing is
# one I’ve spent a bit of time on), you’ll definitely want some tests
# for that.

# Try to write the minimal tests that will give you confidence that
# your design and layout is working, without testing what it actually
# is. Aim to leave yourself in a position where you can freely make
# changes to the design and layout, without having to go back and
# adjust tests all the time.


#       Don’t Forget the “Refactor” in “Red, Green, Refactor”
# A criticism that’s sometimes levelled at TDD is that it leads to
# badly architected code, as the developer just focuses on getting
# tests to pass rather than stopping to think about how the whole
# system should be designed. I think it’s slightly unfair.

# TDD is no silver bullet. You still have to spend time thinking
# about good design. But what often happens is that people forget the
# “Refactor” in “Red, Green, Refactor”. The methodology allows you to
# throw together any old code to get your tests to pass, but it also
# asks you to then spend some time refactoring it to improve its
# design. Otherwise, it’s too easy to allow “technical debt” to build
# up.

# Often, however, the best ideas for how to refactor code don’t occur
# to you straight away. They may occur to you days, weeks, even
# months after you wrote a piece of code, when you’re working on
# something totally unrelated and you happen to see some old code
# again with fresh eyes. But if you’re halfway through something
# else, should you stop to refactor the old code?

# The answer is that it depends. In the case at the beginning of the
# chapter, we haven’t even started writing our new code. We know we
# are in a working state, so we can justify putting a skip on our new
# FT (to get back to fully passing tests) and do a bit of refactoring
# straight away.

# Later in the chapter we’ll spot other bits of code we want to
# alter. In those cases, rather than taking the risk of refactoring
# an application that’s not in a working state, we’ll make a note of
# the thing we want to change on our scratchpad and wait until we’re
# back to a fully passing test suite before refactoring.
