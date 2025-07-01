import mimetypes
from math import ceil

from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage

# import sys
# sys.path.append('../config')
# from settings  import FILE_UPLOAD_MAX_MEMORY_SIZE


def convert_to_megabyte(file_size):
    file_size_in_mb = round(file_size / (1024 * 1024))
    return ceil(file_size_in_mb)


def custom_file_validator(file):

    file_types = ["image/png", "image/bmp", "image/jpeg", "image/jpg", "application/pdf"]

    if not file:
        raise ValidationError("Нет выбраного файла.....")
    FILE_UPLOAD_MAX_MEMORY_SIZE = 30 * 1024 * 1024 # (30 MEGABYTES)
    if file.size > FILE_UPLOAD_MAX_MEMORY_SIZE:
        raise ValidationError(f"Размер файла должен быть меньше чем {convert_to_megabyte(FILE_UPLOAD_MAX_MEMORY_SIZE)}MB.")

    fs = FileSystemStorage()
    filename = fs.save(file.name, file)
    file_type = mimetypes.guess_type(filename)[0]
    if file_type not in file_types:
        raise ValidationError("Неправильный тип файла, загружаются файлы (png, jpg, jpeg, pdf).")
    return file