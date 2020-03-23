from django import forms

from lists.models import Item


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
