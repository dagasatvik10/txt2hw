from unittest.mock import Mock, patch

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from characters.models import Character
from characters.tests.factories import mock_s3_generate_presigned_post
from users.services import user_create

credentials = {"email": "test@satvikdaga.com", "password": "satvikdaga"}


class DirectUploadApiTests(TestCase):
    """
    We want to test the following:

    1. A start-upload-finish cycle
    """

    def setUp(self):
        self.client = APIClient()

        self.direct_upload_start_url = reverse("api:characters:upload:start")
        self.direct_upload_finish_url = reverse("api:characters:upload:finish")

        user_create(**credentials)

        jwt_login_url = reverse("api:authentication:login")
        self.client.post(jwt_login_url, credentials)

    @patch("characters.services.s3_generate_presigned_post", return_value=mock_s3_generate_presigned_post())
    def test_direct_upload_start_creates_character_and_returns_presigned_url(self, mocked: Mock):
        inputs = {"value": "z", "image_name": "z.png", "image_type": "image/png"}

        response = self.client.post(self.direct_upload_start_url, inputs)

        self.assertEqual(200, response.status_code)

        mocked.assert_called_once()

        data = response.data
        # returns presigned url
        self.assertIn("url", data)
        # returns character id
        self.assertIn("id", data)

        # check if character is created for the returned id
        character = Character.objects.get(id=data["id"])
        self.assertEqual(character.value, inputs["value"])
        self.assertEqual(character.original_image_name, inputs["image_name"])
        self.assertIn(str(ord(inputs["value"])), character.image_name)

        # check if character is not valid
        self.assertEqual(character.is_valid, False)
        # check if upload is not finished
        self.assertIsNone(character.upload_finished_at)

    @patch("characters.services.s3_generate_presigned_post", return_value=mock_s3_generate_presigned_post())
    def test_direct_upload_finish_sets_upload_finished_at_field(self, mocked):
        inputs = {"value": "z", "image_name": "z.png", "image_type": "image/png"}

        response = self.client.post(self.direct_upload_start_url, inputs)

        data = response.data

        inputs = {"character_id": data["id"]}

        response = self.client.post(self.direct_upload_finish_url, inputs)

        self.assertEqual(200, response.status_code)

        data = response.data

        character = Character.objects.get(id=data["id"])

        # check if character is valid
        self.assertEqual(character.is_valid, True)
        # check if upload is finished
        self.assertIsNotNone(character.upload_finished_at)
