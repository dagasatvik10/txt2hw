"""account serializers

contains user, register and login serializer
"""
from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """serializer for the user object"""

    class Meta:
        model = get_user_model()
        fields = ("id", "username", "email")


class RegisterSerializer(serializers.ModelSerializer):
    """serializer for register user object"""

    class Meta:
        model = get_user_model()
        fields = ("id", "username", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)  # type: ignore


class LoginSerializer(serializers.Serializer):
    """serializer for the login user object"""

    # pylint: disable=abstract-method
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        user = authenticate(
            request=self.context.get("request"),
            username=username,
            password=password,
        )

        if not user:
            msg = _("Invalid credentials")
            raise serializers.ValidationError(msg, code="authentication")

        return user
