from fastapi import APIRouter, status, Depends, Query
from controller.crud.warning import WarningCrud
from controller.crud.user import UserCrud
from routers.middleware.authorization import verify_user_access_token
from database.session import session
from controller.errors.http.exceptions import bad_request, not_found
from schemas.warning import CreateWarningModel, UpdateWarningModel
from controller.src.warning import create_warning, get_warning_client_data
from controller.src.user import is_parish_leader, is_council_member
from controller.errors.http.exceptions import unauthorized

router = APIRouter()
warning_crud = WarningCrud()
user_crud = UserCrud()

@router.get('/community/warnings', status_code=status.HTTP_200_OK, dependencies=[Depends(verify_user_access_token)], summary="Warnings", description="Get all community warnings")
async def get_ten_community_warnings(total: int = Query(1, ge=1, le=20), user: dict = Depends(verify_user_access_token)):
    user = await user_crud.get_user_by_cpf(session, user['cpf'])
    warnings = await warning_crud.get_warning_by_community_id(session, user.community_id, total)
    new_warning = []
    for warning in warnings:
        new_warning.append(get_warning_client_data(warning))
    return new_warning

@router.get('/community/warning/{warning_id}', status_code=status.HTTP_200_OK, dependencies=[Depends(verify_user_access_token)], summary="Warnings", description="Get warning by id")
async def get_community_warning(warning_id: str | None = None, user: dict = Depends(verify_user_access_token)):
    #if warning_id == None: raise bad_request(f"No warning was send")
    user = await user_crud.get_user_by_cpf(session, user['cpf'])
    warning = await warning_crud.get_warning_by_id(session, warning_id)
    #if user.community_id != warning.community_id: raise not_found("Warning not found")
    return get_warning_client_data(warning)

@router.post('/community/warnings', status_code=status.HTTP_201_CREATED, dependencies=[Depends(verify_user_access_token)], summary="Warnings", description="Create a warning")
async def create_community_warning(warning: CreateWarningModel, user: dict = Depends(verify_user_access_token)):
    #if is_parish_leader(user['position']) or is_council_member(user['position']):
    user = await user_crud.get_user_by_cpf(session, user['cpf'])
    warning = dict(warning)
    warning['community_id'] = user.community_id
    warning = await create_warning(warning)
    warning = await warning_crud.create_warning(session, warning)
    return get_warning_client_data(warning)
    #raise unauthorized(f"You can't create a warning")

@router.put('/community/warnings/{warning_id}', status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(verify_user_access_token)], summary="Warnings", description="Update a warning by id")
async def update_community_warning(warning: UpdateWarningModel, warning_id: str, user: dict = Depends(verify_user_access_token)):
    #if is_parish_leader(user['position']) or is_council_member(user['position']):
    warning = dict(warning)
    warning['id'] = warning_id
    user = await user_crud.get_user_by_cpf(session, user['cpf'])
    db_warning = await warning_crud.get_warning_by_id(session, warning['id'])
    #if user.community_id == db_warning.community_id:
    warning = await warning_crud.update_warning(session, warning)
    return get_warning_client_data(warning)
    #raise unauthorized(f"You can't update this warning")

@router.delete('/community/warnings/{warning_id}', status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(verify_user_access_token)], summary="Warnings", description="Delete a warning by id")
async def delete_community_warning(warning_id: str, user: dict = Depends(verify_user_access_token)):
    # if is_parish_leader(user['position']) or is_council_member(user['position']):
    user = await user_crud.get_user_by_cpf(session, user['cpf'])
    warning = await warning_crud.get_warning_by_id(session, warning_id)
        # if user.community_id == warning.community_id:
    return await warning_crud.delete_warning(session, warning)
    #raise unauthorized(f"You can't delete this warning")