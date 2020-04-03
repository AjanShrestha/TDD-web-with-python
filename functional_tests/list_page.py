from selenium.webdriver.common.keys import Keys

from .base import wait


class ListPage(object):

    def __init__(self, test):
        self.test = test  # 1

    def get_table_rows(self):  # 3
        return self.test.browser.find_elements_by_css_selector('#id_list_table tr')

    @wait
    def wait_for_row_in_list_table(self, item_text, item_number):  # 2
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

    def get_share_box(self):
        return self.test.browser.find_element_by_css_selector(
            'input[name="sharee"]'
        )

    def get_shared_with_list(self):
        return self.test.browser.find_elements_by_css_selector(
            '.list-sharee'
        )

    def share_list_with(self, email):
        self.get_share_box().send_keys(email)
        self.get_share_box().send_keys(Keys.ENTER)
        self.test.wait_for(lambda: self.test.assertIn(
            email,
            [item.text for item in self.get_shared_with_list()]
        ))

        # 1. It’s initialised with an object that represents the current
        #   test. That gives us the ability to make assertions, access
        #   the browser instance via self.test.browser, and use the self.
        #   test.wait_for function.
        # 2. I’ve copied across some of the existing helper methods from
        #   base.py, but I’ve tweaked them slightly...
        # 3. For example, they make use of this new method.
        # 4 Returning self is just a convenience. It enables method
        #   chaining, which we’ll see in action immediately.

    def get_list_owner(self):
        return self.test.browser.find_element_by_id('id_list_owner').text


#                      Page Pattern
# We’ve already built several helper methods for our FTs, including
# add_list_item, which we’ve used here, but if we just keep adding
# more and more, it’s going to get very crowded. I’ve worked on a
# base FT class that was over 1,500 lines long, and that got pretty
# unwieldy.

# Page objects are an alternative which encourage us to store all the
# information and helper methods about the different types of pages
# on our site in a single place.

# The idea behind the Page pattern is that it should capture all the
# information about a particular page in your site, so that if,
# later, you want to go and make changes to that page—even just
# simple tweaks to its HTML layout, for example—you have a single
# place to go to adjust your functional tests, rather than having to
# dig through dozens of FTs.
