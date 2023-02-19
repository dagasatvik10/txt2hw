import mimetypes
from typing import Any, Dict, Tuple

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from characters.models import Character
from characters.utils import bytes_to_mib, file_generate_name, file_generate_upload_path
from integrations.aws.client import s3_generate_presigned_post
from users.models import BaseUser


def _validate_file_size(file_obj):
    max_size = settings.FILE_MAX_SIZE

    if file_obj.size > max_size:
        raise ValidationError(f"File is too large. It should not exceed {bytes_to_mib(max_size)} MiB")


class CharacterStandardUploadService:
    """
    This also serves as an example of a service class,
    which encapsulates 2 different behaviors (create & update) under a namespace.

    Meaning, we use the class here for:

    1. The namespace
    2. The ability to reuse `_infer_file_name_and_type` (which can also be an util)
    """

    def __init__(self, user: BaseUser, image_obj, value: str):
        self.user = user
        self.image_obj = image_obj
        self.value = value

    def _infer_image_name_and_type(self, image_name: str = "", image_type: str = "") -> Tuple[str, str]:
        if not image_name:
            image_name = self.image_obj.name

        if not image_type:
            guessed_image_type, encoding = mimetypes.guess_type(image_name)

            if guessed_image_type is None:
                image_type = ""
            else:
                image_type = guessed_image_type

        return image_name, image_type

    @transaction.atomic
    def create(self, image_name: str = "", image_type: str = "") -> Character:
        _validate_file_size(self.image_obj)

        image_name, image_type = self._infer_image_name_and_type(image_name, image_type)

        obj = Character(
            value=self.value,
            image=self.image_obj,
            original_image_name=image_name,
            image_name=file_generate_name(image_name, self.value),
            image_type=image_type,
            user=self.user,
            upload_finished_at=timezone.now(),
        )

        obj.full_clean()
        obj.save()

        return obj

    @transaction.atomic
    def update(self, character: Character, image_name: str = "", image_type: str = "") -> Character:
        _validate_file_size(self.image_obj)

        image_name, image_type = self._infer_image_name_and_type(image_name, image_type)

        character.image = self.image_obj
        character.original_image_name = image_name
        character.image_name = file_generate_name(image_name, self.value)
        character.image_type = image_type
        character.value = self.value
        character.user = self.user
        character.upload_finished_at = timezone.now()

        character.full_clean()
        character.save()

        return character


class CharacterDirectUploadService:
    def __init__(self, user):
        self.user = user

    @transaction.atomic
    def start(self, *, value: str, image_name: str, image_type: str):
        character = Character(
            value=value,
            original_image_name=image_name,
            image_name=file_generate_name(image_name, value),
            user=self.user,
            image=None,
            image_type=image_type,
        )
        character.full_clean()
        character.save()

        upload_path = file_generate_upload_path(character, character.image_name)

        """
        We are doing this in order to have an associated file for the field.
        """
        character.image = character.image.field.attr_class(character, character.image.field, upload_path)
        character.save()

        presigned_data: Dict[str, Any] = {}

        # if settings.FILE_UPLOAD_STORAGE == FileUploadStorage.s3:
        presigned_data = s3_generate_presigned_post(file_path=upload_path, file_type=image_type)

        return {"id": character.id, **presigned_data}

    @transaction.atomic
    def finish(self, *, character: Character) -> Character:
        # Potentially, check against user
        character.upload_finished_at = timezone.now()
        character.full_clean()
        character.save()

        return character
