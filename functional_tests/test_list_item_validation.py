from selenium.webdriver.common.keys import Keys
from unittest import skip

from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    def get_error_elements(self):
        return self.browser.find_element_by_css_selector('.has-error')
        # I like to keep helper functions in the FT class that’s
        # using them, and only promote them to the base class when
        # they’re actually needed elsewhere. It stops the base class
        # from getting too cluttered. YAGNI.

    def test_cannot_add_empty_list_items(self):
        # Edith goes to the home page and accidentally tries to submit
        # an empty list item. She hits Enter on the empty input box
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)
        # Whenever you submit a form with Keys.ENTER or click
        # something that is going to cause a page to load, you
        # probably want an explicit wait for your next assertion.

        # The browser intercepts the request, and does not load the
        # list page
        self.wait_for(
            lambda:
            self.browser.find_element_by_css_selector(
                '#id_text:invalid')
        )

        # She starts typing some text for the new item and the error
        # disappears
        self.get_item_input_box().send_keys('Buy milk')
        self.wait_for(
            lambda:
            self.browser.find_element_by_css_selector(
                '#id_text:valid')
        )

        # And she can submit it successfully
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # Perversely, she now decies to submit a second blank list
        # item
        self.get_item_input_box().send_keys(Keys.ENTER)

        # Again, the browser will not comply
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for(
            lambda:
            self.browser.find_element_by_css_selector(
                '#id_text:invalid')
        )

        # And she can correct it by filling some text in
        self.get_item_input_box().send_keys('Make tea')
        self.wait_for(
            lambda:
            self.browser.find_element_by_css_selector(
                '#id_text:valid')
        )
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for_row_in_list_table('2: Make tea')

    def test_cannot_add_duplicate_items(self):
        # Edith goes to the home page and starts a new list
        self.browser.get(self.live_server_url)
        self.add_list_item('Buy wellies')

        # She accidentally tries to enter a duplicated item
        self.get_item_input_box().send_keys('Buy wellies')
        self.get_item_input_box().send_keys(Keys.ENTER)

        # She sees a helpful error message
        self.wait_for(lambda: self.assertEqual(
            self.get_error_elements().text,
            "You've already got this in your list"
        ))

    def test_error_messages_are_cleared_on_input(self):
        # Edith starts a list and causes a validation error:
        self.browser.get(self.live_server_url)
        self.add_list_item('Banter too thick')
        self.get_item_input_box().send_keys('Banter too thick')
        self.get_item_input_box().send_keys(Keys.ENTER)

        self.wait_for(lambda: self.assertTrue(
            self.get_error_elements().is_displayed()
        ))

        # She starts typing in the input box to clear the error
        self.get_item_input_box().send_keys('a')

        # She is pleased to see that the error message disappears
        self.wait_for(lambda: self.assertFalse(
            self.get_error_elements().is_displayed()
        ))
