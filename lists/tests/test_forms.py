from django.test import TestCase

from lists.forms import ItemForm


class ItemFormTest(TestCase):

    def test_form_renders_item_text_input(self):
        form = ItemForm()
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())
        # form.as_p() renders the form as HTML.


# Development-Driven Tests: Using Unit Tests for Exploratory Coding
# Does this feel a bit like development-driven tests? That’s OK, now
# and again.

# When you’re exploring a new API, you’re absolutely allowed to mess
# about with it for a while before you get back to rigorous TDD. You
# might use the interactive console, or write some exploratory code
# (but you have to promise the Testing Goat that you’ll throw it away
# and rewrite it properly later).

# Here we’re actually using a unit test as a way of experimenting
# with the forms API. It’s actually a pretty good way of learning how
# it works.
