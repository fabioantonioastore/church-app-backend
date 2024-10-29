from fastapi import File, UploadFile
from models.image import Image


def is_png_or_jpeg_image(file: UploadFile) -> bool:
    return file.content_type == "image/jpeg" or file.content_type == "image/png"


def is_png_image(file: UploadFile) -> bool:
    return file.content_type == "image/png"


def is_jpeg_image(file: UploadFile) -> bool:
    return file.content_type == "image/jpeg"


def get_image_bytes(image: Image):
    return image.byte
