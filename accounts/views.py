from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.contrib import auth, messages
from django.shortcuts import redirect

from accounts.models import Token


def send_login_email(request):
    email = request.POST['email']
    token = Token.objects.create(email=email)
    url = request.build_absolute_uri(
        f"{reverse('login')}?token={str(token.uid)}"
    )
    # request.build_absolute_uri deserves a mention—it’s one way to
    # build a “full” URL, including the domain name and the http(s)
    # part, in Django. There are other ways, but they usually involve
    # getting into the “sites” framework, and that gets
    # overcomplicated pretty quickly.
    message_body = f'Use this link to log in:\n\n{url}'
    send_mail(
        'Your login link for Superlists',
        message_body,
        'noreply@superlists',
        [email],
    )
    messages.success(
        request,
        "Check your email, we've sent you a link you can use to log in."
    )
    return redirect('/')


def login(request):
    auth.authenticate(uid=request.GET.get('token'))
    auth.login('ack!')
    return redirect('/')
