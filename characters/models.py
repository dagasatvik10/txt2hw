from django.conf import settings
from django.db import models

from characters.enums import FileUploadStorage
from characters.utils import file_generate_upload_path
from common.models import BaseModel
from users.models import BaseUser


class Character(BaseModel):
    # handwritten image
    image = models.FileField(upload_to=file_generate_upload_path, blank=True, null=True)

    original_image_name = models.TextField()

    image_name = models.CharField(max_length=255, unique=True)
    image_type = models.CharField(max_length=255)

    # character value
    value = models.CharField(max_length=1)

    user = models.ForeignKey(BaseUser, null=True, on_delete=models.SET_NULL)

    upload_finished_at = models.DateTimeField(blank=True, null=True)

    @property
    def is_valid(self):
        """
        We consider an image "valid" if the "upload_finished_at" flag has value
        """
        return bool(self.upload_finished_at)

    @property
    def url(self):
        """
        Get image url
        """
        if settings.FILE_UPLOAD_STORAGE == FileUploadStorage.S3:
            return self.image.url

        return f"{settings.APP_DOMAIN}{self.image.url}"
