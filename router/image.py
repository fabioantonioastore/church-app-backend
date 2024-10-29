from fastapi import File, UploadFile, APIRouter, Depends, status
from router.middleware.authorization import verify_user_access_token
from fastapi.responses import StreamingResponse
from io import BytesIO
from controller.src.image import is_png_or_jpeg_image
from controller.errors.http.exceptions import not_acceptable
from controller.crud.user import UserCrud
from controller.crud.community import CommunityCrud

user_crud = UserCrud()
community_crud = CommunityCrud()

router = APIRouter()


@router.patch("/image/community", status_code=status.HTTP_204_NO_CONTENT,
              dependencies=[Depends(verify_user_access_token)])
async def upload_community_image(user: dict = Depends(verify_user_access_token), file: UploadFile = File(...)):
    if is_png_or_jpeg_image(file):
        image_data = await file.read()
        user = await user_crud.get_user_by_cpf(user['cpf'])
        await community_crud.update_community_image(user.community_id, image_data)


@router.get("/image/community", status_code=status.HTTP_200_OK, dependencies=[Depends(verify_user_access_token)])
async def get_community_image(user: dict = Depends(verify_user_access_token), file: UploadFile = File(...)):
    user = await user_crud.get_user_by_cpf(user['cpf'])
    image = await community_crud.get_community_image(user.community_id)
    image = BytesIO(image)
    return StreamingResponse(image, media_type="image/jpeg")


@router.patch("/image/user", status_code=status.HTTP_204_NO_CONTENT,
              dependencies=[Depends(verify_user_access_token)])
async def upload_user_image(user: dict = Depends(verify_user_access_token), file: UploadFile = File(...)):
    if is_png_or_jpeg_image(file):
        image_data = await file.read()
        user = await user_crud.update_user_image(user['cpf'], image_data)
        return
    raise not_acceptable("Invalid content type")


@router.get('/image/user', status_code=status.HTTP_200_OK, dependencies=[Depends(verify_user_access_token)])
async def get_user_image(user: dict = Depends(verify_user_access_token)):
    image = await user_crud.get_user_image(user['cpf'])
    image = BytesIO(image)
    return StreamingResponse(image, media_type="image/jpeg")
