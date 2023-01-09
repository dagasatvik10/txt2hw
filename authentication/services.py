from django.contrib.auth.signals import user_logged_out
from rest_framework.request import Request


def auth_logout(*, request: Request):
    request._auth.delete()
    user_logged_out.send(sender=request.user.__class__, request=request, user=request.user)
