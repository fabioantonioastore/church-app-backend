from fastapi import File, UploadFile


def verify_if_file_is_png_or_jpeg(file: UploadFile) -> bool:
    return file.content_type == "image/jpeg" or file.content_type == "image/png"


def is_png_image(file: UploadFile) -> bool:
    return file.content_type == "image/png"


def is_jpeg_image(file: UploadFile) -> bool:
    return file.content_type == "image/jpeg"
