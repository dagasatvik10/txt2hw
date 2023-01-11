# from knox.models import AuthToken
from django.conf import settings
from django.contrib.auth import login
from knox.views import LoginView as KnoxLoginView
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.mixins import ApiAuthMixin
from authentication.serializers import AuthTokenSerializer
from authentication.services import auth_logout
from users.selectors import user_get_login_data


class UserMeAPI(ApiAuthMixin, APIView):
    def get(self, request, *args, **kwargs):
        data = user_get_login_data(user=request.user)

        return Response(data)


class UserJwtLoginApi(KnoxLoginView):
    authentication_classes = []
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = AuthTokenSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data["user"]
            login(request, user)
            response = super().post(request, *args, **kwargs)
            response.set_cookie(
                key=settings.AUTH_JWT_COOKIE_KEY,
                value=response.data["token"],
                expires=settings.REST_KNOX["TOKEN_TTL"],
                secure=settings.AUTH_JWT_COOKIE_SECURE,
                httponly=True,
                samesite=settings.AUTH_JWT_COOKIE_SAMESITE,
            )
            response.data = {"message": "Login successful", "data": response.data}
            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserJwtLogoutApi(ApiAuthMixin, APIView):
    def post(self, request, *args, **kwargs):
        auth_logout(request=request)
        response = Response(None, status=status.HTTP_204_NO_CONTENT)

        if settings.AUTH_JWT_COOKIE_KEY is not None:
            response.delete_cookie(settings.AUTH_JWT_COOKIE_KEY)

        return response
