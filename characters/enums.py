from enum import Enum


class FileUploadStorage(Enum):
    LOCAL = "local"
    S3 = "s3"
