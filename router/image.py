from fastapi import File, UploadFile, APIRouter, Depends, status
from router.middleware.authorization import verify_user_access_token
from controller.src.image import is_png_or_jpeg_image
from controller.errors.http.exceptions import not_acceptable
from controller.crud.user import UserCrud
from controller.crud.community import CommunityCrud
from io import BytesIO
from fastapi.responses import StreamingResponse
from controller.crud.image import ImageCrud
from controller.src.image import get_image_bytes, create_image

user_crud = UserCrud()
community_crud = CommunityCrud()
image_crud = ImageCrud()

router = APIRouter()


@router.patch("/image/community", status_code=status.HTTP_204_NO_CONTENT,
              dependencies=[Depends(verify_user_access_token)])
async def upload_community_image(user: dict = Depends(verify_user_access_token), file: UploadFile = File(...)):
    if is_png_or_jpeg_image(file):
        user = await user_crud.get_user_by_cpf(user['cpf'])
        community = await community_crud.get_community_by_id(user.id)
        if community.image:
            await image_crud.delete_image_by_id(community.image)
        image_data = await file.read()
        image = await create_image(image_data)
        await community_crud.update_community_image(community.id, image.id)
    raise not_acceptable("Invalid content type")


@router.get("/image/community", status_code=status.HTTP_200_OK, dependencies=[Depends(verify_user_access_token)])
async def get_community_image(user: dict = Depends(verify_user_access_token)):
    user = await user_crud.get_user_by_cpf(user['cpf'])
    community = await community_crud.get_community_by_id(user.community_id)
    image = await image_crud.get_image_by_id(community.image)
    image = BytesIO(get_image_bytes(image))
    return StreamingResponse(image, media_type="image/jpeg")


@router.patch("/image/user", status_code=status.HTTP_204_NO_CONTENT,
              dependencies=[Depends(verify_user_access_token)])
async def upload_user_image(user: dict = Depends(verify_user_access_token), file: UploadFile = File(...)):
    if is_png_or_jpeg_image(file):
        user = await user_crud.get_user_by_cpf(user['cpf'])
        if user.image:
            await image_crud.delete_image_by_id(user.image)
        image_data = await file.read()
        image = await create_image(image_data)
        await user_crud.update_user_image(user.cpf, image.id)
        return
    raise not_acceptable("Invalid content type")


@router.get('/image/user', status_code=status.HTTP_200_OK, dependencies=[Depends(verify_user_access_token)])
async def get_user_image(user: dict = Depends(verify_user_access_token)):
    user = await user_crud.get_user_by_cpf(user['cpf'])
    image = await image_crud.get_image_by_id(user.image)
    image = BytesIO(get_image_bytes(image))
    return StreamingResponse(image, media_type="image/jpeg")