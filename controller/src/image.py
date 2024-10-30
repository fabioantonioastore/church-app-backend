import base64
from fastapi import File, UploadFile
from models.image import Image
from controller.crud.image import ImageCrud

image_crud = ImageCrud()


def is_png_or_jpeg_image(file: UploadFile) -> bool:
    return file.content_type == "image/jpeg" or file.content_type == "image/png"


def is_png_image(file: UploadFile) -> bool:
    return file.content_type == "image/png"


def is_jpeg_image(file: UploadFile) -> bool:
    return file.content_type == "image/jpeg"


def get_image_bytes(image: Image):
    return image.byte


async def create_image(image_data) -> Image:
    image = Image()
    image.byte = image_data
    return await image_crud.create_image(image)


def convert_image_to_base64(image_data):
    return base64.b64encode(image_data).decode('utf-8')
