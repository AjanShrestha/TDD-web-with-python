# Django's MVC, URLs, and View Functions
# Django is structured along a classic Model-View-Controller (MVC)
# pattern. It definitely does have models, but its views are more
# like a controller, and it's the templates that are actually the
# view part, but the general idea is there.

# As with any web server, Django's main job is to decide what to do
# when a user asks for a particular URL on our site. Django's workfow
# goes something like this:
# 1. An HTTP request comes in for a particular URL.
# 2. Django uses some rules to decide which view function should deal
#   with the request (this is referred to as resolving the URL).
# 3. The view function processes the request and returns an HTTP
#   response.

from django.http import HttpResponse
from django.shortcuts import redirect, render

from lists.models import Item, List

# Create your views here.


def home_page(request):
    # Refactor
    # When we try to improve the code without changing its
    # functionality
    # When refactoring, work on either the code or the tests, but not
    # both at once.
    return render(request, 'home.html')
    # Instead of building our own HttpResponse, we now use the Django
    # render function. It takes the request as its first parameter
    # and the name of the template to render. Django will
    # automatically search folders called templates inside any of
    # your apps’ directories. Then it builds an HttpResponse for you,
    # based on the content of the template.
    # Templates are a very powerful feature of Django’s, and their
    # main strength consists of substituting Python variables into
    # HTML text.


def new_list(request):
    list_ = List.objects.create()
    item = Item.objects.create(text=request.POST['item_text'], list=list_)
    item.full_clean()
    return redirect(f'/lists/{list_.id}/')


def add_item(request, list_id):
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect(f'/lists/{list_.id}/')


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    return render(request, 'list.html', {'list': list_})
