"""account apis

contains register and login user api
"""
from knox.models import AuthToken
from rest_framework import generics, permissions
from rest_framework.response import Response

from .serializers import LoginSerializer, RegisterSerializer, UserSerializer


class RegisterAPI(generics.GenericAPIView):
    """api to register new user"""

    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        """creates a new user and returns the new user and its auth token"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        token = AuthToken.objects.create(user)[1]

        return Response({"user": UserSerializer(user, context=self.get_serializer_context()).data, "token": token})


class LoginAPI(generics.GenericAPIView):
    """api to authenticate a user"""

    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        """returns the authenticated user"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data
        token = AuthToken.objects.create(user)[1]

        return Response({"user": UserSerializer(user, context=self.get_serializer_context()).data, "token": token})


class UserAPI(generics.RetrieveAPIView):
    """api to fetch the logged in user"""

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
