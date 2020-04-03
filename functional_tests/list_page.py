from selenium.webdriver.common.keys import Keys

from .base import wait:


class ListPage(object):

    def __init__(self, test):
        self.test = test  # 1

    def get_table_rows(self):  # 3
        return self.test.browser.find_elements_by_css_selector('#id_list_table tr')

    @wait
    def wait_for_row_in_list_table(self, item_next, item_number):  # 2
        expected_row_text = f'{item_number}: {item_text}'
        rows = self.get_table_rows()
        self.test.assertIn(expected_row_text, [row.text for row in rows])

    def get_item_input_box(self):  # 2
        return self.test.browser.find_element_by_id('id_text')

    def add_list_item(self, item_text):  # 2
        new_item_no = len(self.get_table_rows()) + 1
        self.get_item_input_box().send_keys(item_text)
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table(item_text, new_item_no)
        return self  # 4

    # 1. It’s initialised with an object that represents the current
    #   test. That gives us the ability to make assertions, access
    #   the browser instance via self.test.browser, and use the self.
    #   test.wait_for function.
    # 2. I’ve copied across some of the existing helper methods from
    #   base.py, but I’ve tweaked them slightly...
    # 3. For example, they make use of this new method.
    # 4 Returning self is just a convenience. It enables method
    #   chaining, which we’ll see in action immediately.
