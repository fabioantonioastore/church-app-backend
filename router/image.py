from fastapi import File, UploadFile, APIRouter, Depends, status
from router.middleware.authorization import verify_user_access_token
from controller.src.image import is_png_or_jpeg_image
from controller.errors.http.exceptions import not_acceptable
from controller.crud.user import UserCrud
from controller.crud.community import CommunityCrud
from controller.crud.image import ImageCrud
from controller.src.image import create_image, convert_image_to_base64

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
            community.image = None
        image_data = await file.read()
        image = await create_image(image_data)
        await community_crud.update_community_image(community.id, image.id)
    raise not_acceptable("Invalid content type")


@router.get("/image/community", status_code=status.HTTP_200_OK, dependencies=[Depends(verify_user_access_token)])
async def get_community_image(user: dict = Depends(verify_user_access_token)):
    user = await user_crud.get_user_by_cpf(user['cpf'])
    community = await community_crud.get_community_by_id(user.community_id)
    if community.image:
        image = await image_crud.get_image_by_id(community.image)
        image_base64 = convert_image_to_base64(image.byte)
        return {"image": image_base64}
    return None


@router.patch("/image/user/{cpf}", status_code=status.HTTP_204_NO_CONTENT,
              dependencies=[Depends(verify_user_access_token)])
async def upload_user_image(cpf: str, user: dict = Depends(verify_user_access_token), file: UploadFile = File(...)):
    if is_png_or_jpeg_image(file):
        user_cpf = await user_crud.get_user_by_cpf(cpf)
        if user_cpf.image:
            await image_crud.delete_image_by_id(user_cpf.image)
            user_cpf.image = None
        image_data = await file.read()
        image = await create_image(image_data)
        await user_crud.update_user_image(user_cpf.cpf, image.id)
        return
    raise not_acceptable("Invalid content type")


@router.get('/image/user/{cpf}', status_code=status.HTTP_200_OK, dependencies=[Depends(verify_user_access_token)])
async def get_user_image(cpf: str, user: dict = Depends(verify_user_access_token)):
    user_cpf = await user_crud.get_user_by_cpf(cpf)
    if user_cpf.image:
        image = await image_crud.get_image_by_id(user_cpf.image)
        image_base64 = convert_image_to_base64(image.byte)
        return {"image": image_base64}
    return None


@router.delete('/image/user/{cpf}', status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(verify_user_access_token)])
async def delete_user_image(cpf: str, user: dict = Depends(verify_user_access_token)):
    user_cpf = await user_crud.get_user_by_cpf(cpf)
    if user_cpf.image:
        await image_crud.delete_image_by_id(user_cpf.image)
        await user_crud.delete_user_image(user_cpf.id)
