from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models

# Create your models here.


class List(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('view_list', args=[self.id])

    @property
    def name(self):
        return self.item_set.first().text

    #   The @property Decorator in Python
    # If you haven’t seen it before, the @property decorator
    # transforms a method on a class to make it appear to the outside
    # world like an attribute.
    # This is a powerful feature of the language, because it makes it
    # easy to implement “duck typing”, to change the implementation
    # of a property without changing the interface of the class. In
    # other words, if we decide to change .name into being a “real”
    # attribute on the model, which is stored as text in the
    # database, then we will be able to do so entirely
    # transparently—as far as the rest of our code is concerned, they
    # will still be able to just access .name and get the list name,
    # without needing to know about the implementation. Raymond
    # Hettinger gave a great, beginner-friendly talk on this topic at
    # Pycon a few years ago, which I enthusiastically recommend (it
    # covers about a million good practices for Pythonic class design
    # besides).
    # Of course, in the Django template language, .name would still
    # call the method even if it didn’t have @property, but that’s a
    # particularity of Django, and doesn’t apply to Python in general.


class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None)

    class Meta:
        ordering = ('id',)
        unique_together = ('list', 'text')

    def __str__(self):
        return self.text
