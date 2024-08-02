from fastapi import APIRouter, Request, status, Depends
from routers.middleware.authorization import verify_user_access_token
from controller.crud.user import UserCrud
from controller.crud.login import LoginCrud
from controller.crud.community import CommunityCrud
from database.session import session
from controller.src.user import (get_user_client_data, update_user_name, update_user_email,
                                 update_user_community, update_user_birthday, update_user_image)
from controller.auth.cpf_cryptography import get_crypted_cpf
from schemas.user import (UpdateUserPassword, UpdateUserName, UpdateUserEmail,
                          UpdateUserCommunity, UpdateUserImage, UpdateUserBirthday)
from controller.validators.password import PasswordValidator
from controller.validators.name import NameValidator
from controller.validators.email import EmailValidator
from controller.validators.date import DateValidator
from controller.src.login import update_login_password

router = APIRouter()
user_crud = UserCrud()
login_crud = LoginCrud()
community_crud = CommunityCrud()

@router.get('/me', status_code=status.HTTP_200_OK, dependencies=[Depends(verify_user_access_token)])
async def get_user_data(user: dict = Depends(verify_user_access_token)):
    user = await user_crud.get_user_by_cpf(session, get_crypted_cpf(user['cpf']))
    user = await get_user_client_data(user)
    return user

@router.patch('/me/password', status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(verify_user_access_token)])
async def patch_user_password(password_data: UpdateUserPassword, user: dict = Depends(verify_user_access_token)):
    PasswordValidator(password_data.password)
    login = await login_crud.get_login_by_cpf(session, user['cpf'])
    login = update_login_password(login, password_data.password)
    await login_crud.update_login(session, login)
    return {"password updated"}

@router.patch('/me/name', status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(verify_user_access_token)])
async def patch_user_name(name_data: UpdateUserName, user: dict = Depends(verify_user_access_token)):
    NameValidator(name_data.name)
    user = await user_crud.get_user_by_cpf(session, get_crypted_cpf(user['cpf']))
    user = update_user_name(user, name_data.name)
    await user_crud.update_user(session, user)
    return {"name updated"}

@router.patch('/me/email', status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(verify_user_access_token)])
async def patch_user_email(email_data: UpdateUserEmail, user: dict = Depends(verify_user_access_token)):
    EmailValidator(email_data.email)
    user = await user_crud.get_user_by_cpf(session, get_crypted_cpf(user['cpf']))
    user = update_user_email(user, email_data.email)
    await user_crud.update_user(session, user)
    return {"email updated"}

@router.patch('/me/community', status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(verify_user_access_token)])
async def patch_user_community(community_data: UpdateUserCommunity, user: dict = Depends(verify_user_access_token)):
    community = await community_crud.get_community_by_patron(session, community_data.patron)
    user = await user_crud.get_user_by_cpf(session, get_crypted_cpf(user['cpf']))
    user = update_user_community(user, community.id)
    await user_crud.update_user(session, user)
    return {"community updated"}

@router.patch('/me/image', status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(verify_user_access_token)])
async def patch_user_image(image_data: UpdateUserImage, user: dict = Depends(verify_user_access_token)):
    user = await user_crud.get_user_by_cpf(session, get_crypted_cpf(user['cpf']))
    user = update_user_image(user, image_data.image)
    await user_crud.update_user(session, user)
    return {"user image updated"}

@router.patch('/me/birthday', status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(verify_user_access_token)])
async def patch_user_birthday(birthday_data: UpdateUserBirthday, user: dict = Depends(verify_user_access_token)):
    DateValidator(birthday_data.birthday)
    user = await user_crud.get_user_by_cpf(session, get_crypted_cpf(user['cpf']))
    user = update_user_birthday(user, birthday_data.birthday)
    await user_crud.update_user(session, user)
    return {"birthday updated"}