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

from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import redirect, render

from lists.forms import ExistingListItemForm, ItemForm, NewListForm
from lists.models import List

User = get_user_model()


def home_page(request):
    # Refactor
    # When we try to improve the code without changing its
    # functionality
    # When refactoring, work on either the code or the tests, but not
    # both at once.
    return render(request, 'home.html', {'form': ItemForm()})
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
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List()
        list_.owner = request.user
        list_.save()
        form.save(for_list=list_)
        return redirect(list_)
    else:
        return render(request, 'home.html', {"form": form})


def new_list2(request):
    form = NewListForm(data=request.POST)
    form.save(owner=request.user)


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=list_)
    if request.method == 'POST':
        form = ExistingListItemForm(for_list=list_, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(list_)
    return render(
        request,
        'list.html',
        {'list': list_, "form": form}
    )


def my_lists(request, email):
    owner = User.objects.get(email=email)
    return render(request, 'my_lists.html', {'owner': owner})


# Our two views are now looking very much like “normal” Django views:
# * they take information from a user’s request,
# * combine it with some custom logic or information from the URL
#    (list_id),
# * pass it to a form for validation and possible saving, and
# * then redirect or render a template.


#   A Decision Point: Whether to Proceed to the Next Layer with a Failing Test

# In order to get this test passing, as it’s written now, we have to
# move down to the model layer. However, it means doing more work
# with a failing test, which is not ideal.

# The alternative is to rewrite the test to make it more isolated
# from the level below, using mocks.

# On the one hand, it’s a lot more effort to use mocks, and it can
# lead to tests that are harder to read. On the other hand, imagine
# if our app was more complex, and there were several more layers
# between the outside and the inside. Imagine leaving three or four
# or five layers of tests, all failing while we wait to get to the
# bottom layer to imple‐ ment our critical feature. While tests are
# failing, we’re not sure that layer really works, on its own terms,
# or not. We have to wait until we get to the bottom layer.

# This is a decision point you’re likely to run into in your own
# projects. Let’s investigate both approaches. We’ll start by taking
# the shortcut, and leaving the test failing. In the next chapter,
# we’ll come back to this exact point, and investigate how things
# would have gone if we’d used more isolation.
