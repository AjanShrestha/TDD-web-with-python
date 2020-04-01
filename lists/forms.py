from django import forms
from django.core.exceptions import ValidationError

from lists.models import Item, List


DUPLICATE_ITEM_ERROR = "You've already got this in your list"
EMPTY_ITEM_ERROR = "You can't have an empty list item"


class ItemForm(forms.models.ModelForm):
    # ModelForms do all sorts of smart stuff, like assigning sensible
    # HTML form input types to different types of field, and applying
    # default validation.
    class Meta:
        model = Item
        fields = ('text',)
        # In Meta we specify which model the form is for, and which
        # fields we want it to use.
        widgets = {
            'text': forms.fields.TextInput(attrs={
                'placeholder': 'Enter a to-do item',
                'class': 'form-control input-lg'
            }),
        }
        error_messages = {
            'text': {'required': EMPTY_ITEM_ERROR}
        }

    def save(self, for_list):
        self.instance.list = for_list
        return super().save()
        # The .instance attribute on a form represents the database
        # object that is being modi‐ fied or created.


class NewListForm(ItemForm):

    def save(self, owner):
        if owner.is_authenticated:
            List.create_new(
                first_item_text=self.cleaned_data['text'],
                owner=owner
            )
        else:
            List.create_new(first_item_text=self.cleaned_data['text'])


class ExistingListItemForm(ItemForm):
    def __init__(self, for_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.list = for_list

    def validate_unique(self):
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            e.error_dict = {'text': [DUPLICATE_ITEM_ERROR]}
            self._update_errors(e)

    def save(self):
        return forms.models.ModelForm.save(self)


#           Hiding ORM Code Behind Helper Methods
# One of the techniques that emerged from our use of isolated tests
# was the “ORM helper method”.

# Django’s ORM lets you get things done quickly with a reasonably
# readable syntax (it’s certainly much nicer than raw SQL!). But some
# people like to try to minimise the amount of ORM code in the
# application—particularly removing it from the views and forms
# layers.

# One reason is that it makes it much easier to test those layers.
# But another is that it forces us to build helper functions that
# express our domain logic more clearly. Compare:
        # list_ = List()
        # list_.save()
        # item = Item()
        # item.list = list_
        # item.text = self.cleaned_data['text']
        # item.save()
# With:
        # List.create_new(first_item_text=self.cleaned_data['text']
# This applies to read queries as well as write. Imagine something
# like this:
        # Book.objects.filter(in_print=True, pub_date__lte=datetime.
        # today())
# Versus a helper method, like:
        # Book.all_available_books()
# When we build helper functions, we can give them names that express
# what we are doing in terms of the business domain, which can
# actually make our code more legi‐ ble, as well as giving us the
# benefit of keeping all ORM calls at the model layer, and thus
# making our whole application more loosely coupled.
