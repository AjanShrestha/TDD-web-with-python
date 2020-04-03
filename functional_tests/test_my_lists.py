from .base import FunctionalTest


class MyListsTest(FunctionalTest):

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        # Edith is a logged-in user
        self.create_pre_authenticated_session('edith@example.com')

        # She goes to the home page and starts a list
        self.browser.get(self.live_server_url)
        self.add_list_item('Reticulate splines')
        self.add_list_item('Immanentize eschanton')
        first_list_url = self.browser.current_url

        # She notices a "My lists" link, for the first time.
        self.browser.find_element_by_link_text('My lists').click()

        # She sees that her list is in there, named according to its
        # first list item
        self.wait_for(
            lambda: self.browser.find_element_by_link_text(
                'Reticulate splines')
        )
        self.browser.find_element_by_link_text('Reticulate splines').click()
        self.wait_for(
            lambda: self.assertEqual(
                self.browser.current_url,
                first_list_url
            )
        )

        # She decides to start another list, just to see
        self.browser.get(self.live_server_url)
        self.add_list_item('Click cows')
        second_list_url = self.browser.current_url

        # Under "my lists", her new list appears
        self.browser.find_element_by_link_text('My lists').click()
        self.wait_for(
            lambda: self.browser.find_element_by_link_text('Click cows')
        )
        self.browser.find_element_by_link_text('Click cows').click()
        self.wait_for(
            lambda: self.assertEqual(
                self.browser.current_url,
                second_list_url
            )
        )

        # She logs out. The "My lists" option disappears
        self.browser.find_element_by_link_text("Log out").click()
        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_elements_by_link_text('My lists'),
                []
            )
        )


#       JSON test Fixtures Considered Harmful

# When we pre-populate the database with test data, as we’ve done
# here with the User object and its associated Session object, what
# we’re doing is setting up a “test fixture”.

# Django comes with built-in support for saving database objects as
# JSON (using the manage.py dumpdata), and automatically loading them
# in your test runs using the fixtures class attribute on TestCase.

# More and more people are starting to say: don’t use JSON fixtures.
# They’re a nightmare to maintain when your model changes. Plus it’s
# difficult for the reader to tell which of the many attribute values
# specified in the JSON are critical for the behaviour under test,
# and which are just filler. Finally, even if tests start out sharing
# fixtures, sooner or later one test will want slightly different
# versions of the data, and you end up copying the whole thing around
# to keep them isolated, and again it’s hard to tell what’s relevant
# to the test and what is just happenstance.

# It’s usually much more straightforward to just load the data
# directly using the Django ORM.

# Once you have more than a handful of fields on a model, and/or
# several related models, even using the ORM can be cumbersome. In
# this case, there’s a tool that lots of people swear by called
# factory_boy.
