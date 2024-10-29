from fastapi import File, UploadFile, APIRouter, Depends, status
from router.middleware.authorization import verify_user_access_token
import os
from controller.src.image import is_png_image, is_jpeg_image
from controller.errors.http.exceptions import not_acceptable
from controller.crud.user import UserCrud

user_crud = UserCrud()

router = APIRouter()


@router.put("/upload/image/user", status_code=status.HTTP_204_NO_CONTENT,
            dependencies=[Depends(verify_user_access_token)])
async def upload_image(user: Depends(verify_user_access_token), file: UploadFile = File(...)):
    if is_png_image(file) or is_jpeg_image(file):
        image_data = await file.read()
        user = await user_crud.update_user_image(user['cpf'], image_data)
        return
    raise not_acceptable("Invalid content type")
