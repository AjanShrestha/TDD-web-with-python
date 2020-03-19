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


from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        # The only exception tearDown doesn't run is if an exception
        # inside setUp
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edith has heard about a cool new online to-do-app. She goes
        # to check out its homepage
        self.browser.get('http://localhost:8000')

        # She notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test!')

        # She is invited to enter a to-do item straight away

        # She types "Buy peacock feathers" into a text box (Edith's
        # hobby is tying fly-fishing lures)

        # When she hits enter, the page updates, and now the page
        # lists "1: Buy peacock feathers" as an iem in a to-do list

        # There is still a text box inviting her to add another item.
        # She enters "Use peacock feathers to make a fly" (Edith is
        # very methodical)

        # The page updatees again, and now shows both items on her
        # list

        # Edith wonders whether the still will remember her list.
        # Then she sees that the site has generated a unique URL for
        # her --  there is some explanatory ext to that effect.

        # She visits that URL - her to-do list is still there.

        # Satisfied, she goes back to sleep


if __name__ == "__main__":
    unittest.main()

# First functional test (FT)
# What it's doing
#   Starting a Selenium "webdriver" to pop up a real Firefix browser
#       window
#   Using it to open up a web page which we're expecting to be served
#       from the local PC
#   Checking (making a test assertion) that the page has the word
#       "Django" in its title
