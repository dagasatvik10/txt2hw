import pathlib


def file_generate_name(original_file_name: str, character_value: str):
    extension = pathlib.Path(original_file_name).suffix

    return f"{ord(character_value)}{extension}"


def file_generate_upload_path(instance, filename):
    return f"files/{instance.user.id}/{instance.image_name}"


def bytes_to_mib(value: int) -> float:
    # 1 bytes = 9.5367431640625E-7 mebibytes
    return value * 9.5367431640625e-7
