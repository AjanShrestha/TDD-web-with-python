from django.test import TestCase

from lists.forms import EMPTY_ITEM_ERROR, ItemForm
from lists.models import Item, List


class ItemFormTest(TestCase):

    def test_form_renders_item_text_input(self):
        form = ItemForm()
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())
        # form.as_p() renders the form as HTML.

    def test_form_validation_for_blank_items(self):
        form = ItemForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['text'],
            [EMPTY_ITEM_ERROR]
        )

    def test_form_handles_saving_to_a_list(self):
        list_ = List.objects.create()
        form = ItemForm(data={'text': 'do me'})
        new_item = form.save(for_list=list_)
        self.assertEqual(new_item, Item.objects.first())
        self.assertEqual(new_item.text, 'do me')
        self.assertEqual(new_item.list, list_)


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
