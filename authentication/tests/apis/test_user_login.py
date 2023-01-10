from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from users.models import BaseUser
from users.services import user_create


class UserJwtLoginTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.jwt_login_url = reverse("api:authentication:login")
        self.jwt_logout_url = reverse("api:authentication:logout")
        self.profile_url = reverse("api:authentication:profile")

    def test_non_existing_user_cannot_login(self):
        self.assertEqual(0, BaseUser.objects.count())

        data = {"email": "test@satvikdaga.com", "password": "satvikdaga"}

        response = self.client.post(self.jwt_login_url, data)

        self.assertEqual(400, response.status_code)

    def test_existing_user_can_login_and_access_apis(self):
        """
        1. Create user
        2. Assert login is OK
        3. Call /api/auth/profile
        4. Assert valid response
        """

        credentials = {"email": "test@satvikdaga.com", "password": "satvikdaga"}

        user_create(**credentials)

        response = self.client.post(self.jwt_login_url, credentials)

        self.assertEqual(200, response.status_code)

        data = response.data["data"]
        self.assertIn("token", data)
        token = data["token"]

        jwt_cookie = response.cookies.get(settings.AUTH_JWT_COOKIE_KEY)

        self.assertEqual(token, jwt_cookie.value)

        response = self.client.get(self.profile_url)
        self.assertEqual(200, response.status_code)

        # Now, try without session attached to the client
        client = APIClient()

        response = client.get(self.profile_url)
        self.assertEqual(401, response.status_code)

    def test_existing_user_can_logout(self):
        """
        1. Create user
        2. Login, can access APIs
        3. Logout, cannot access APIs
        """

        credentials = {"email": "test@satvikdaga.com", "password": "satvikdaga"}

        user = user_create(**credentials)

        response = self.client.post(self.jwt_login_url, credentials)
        self.assertEqual(200, response.status_code)

        # assert auth token count for logged in user
        auth_token_count = user.auth_token_set.count()
        self.assertEqual(1, auth_token_count)

        # can access APIs after login
        response = self.client.get(self.profile_url)
        self.assertEqual(200, response.status_code)

        response = self.client.post(self.jwt_logout_url)
        self.assertEqual(204, response.status_code)

        # cannot access APIs after logout
        response = self.client.get(self.profile_url)
        self.assertEqual(401, response.status_code)

        # assert auth token count for logged out user
        auth_token_count = user.auth_token_set.count()
        self.assertEqual(0, auth_token_count)
