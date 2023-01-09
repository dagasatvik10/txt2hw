from django.conf import settings
from knox.auth import TokenAuthentication as KnoxTokenAuthentication
from rest_framework import HTTP_HEADER_ENCODING
from rest_framework.request import Request


def get_authorization_token(request: Request):
    auth = request.COOKIES.get(settings.AUTH_JWT_COOKIE_KEY, b"")
    if isinstance(auth, str):
        # Work around for django test client oddness
        auth = auth.encode(HTTP_HEADER_ENCODING)
    return auth


class TokenAuthentication(KnoxTokenAuthentication):
    def authenticate(self, request):
        auth = get_authorization_token(request)

        if not auth:
            return None

        user, auth_token = self.authenticate_credentials(auth)
        return (user, auth_token)
