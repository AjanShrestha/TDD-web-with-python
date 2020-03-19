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
from django.shortcuts import render

# Create your views here.


def home_page(request):
    return HttpResponse('<html><title>To-Do lists</title></html>')
