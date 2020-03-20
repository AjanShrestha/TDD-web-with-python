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


from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
import time


MAX_WAIT = 10


class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        # The only exception tearDown doesn't run is if an exception
        # inside setUp
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edith has heard about a cool new online to-do-app. She goes
        # to check out its homepage
        self.browser.get(self.live_server_url)

        # She notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # She is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # She types "Buy peacock feathers" into a text box (Edith's
        # hobby is tying fly-fishing lures)
        inputbox.send_keys('Buy peacock feathers')

        # When she hits enter, the page updates, and now the page
        # lists "1: Buy peacock feathers" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # There is still a text box inviting her to add another item.
        # She enters "Use peacock feathers to make a fly" (Edith is
        # very methodical)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, and now shows both items on her
        # list
        self.wait_for_row_in_list_table('1: Buy peacock feathers')
        self.wait_for_row_in_list_table(
            '2: Use peacock feathers to make a fly')

        # Edith wonders whether the still will remember her list.
        # Then she sees that the site has generated a unique URL for
        # her --  there is some explanatory ext to that effect.
        self.fail('Finish the test!')

        # She visits that URL - her to-do list is still there.

        # Satisfied, she goes back to sleep


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
