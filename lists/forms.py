from django import forms
from django.core.exceptions import ValidationError

from lists.models import Item


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
