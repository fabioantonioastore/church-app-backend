from fastapi import APIRouter, status, Depends, Query
from controller.crud import WarningCrud
from controller.crud import UserCrud
from controller.crud import CommunityCrud
from router.middleware.authorization import verify_user_access_token
from schemas.warning import CreateWarningModel, UpdateWarningModel
from controller.src.warning import create_warning, get_warning_client_data
from controller.validators.warning import WarningValidator
from controller.src.web_push_notification import (
    send_notification_to_user,
    MessageNotification,
)

router = APIRouter()
warning_crud = WarningCrud()
user_crud = UserCrud()
community_crud = CommunityCrud()


@router.get(
    "/community/warnings/{community_patron}",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(verify_user_access_token)],
    summary="Warnings",
    description="Get all community warnings",
)
async def get_ten_community_warnings(
    community_patron: str,
    total: int = Query(default=10, ge=1),
    user: dict = Depends(verify_user_access_token),
):
    community = await community_crud.get_community_by_patron(community_patron)
    warnings = await warning_crud.get_warning_by_community_id(
        community.id, total
    )
    new_warning = []
    for warning in warnings:
        new_warning.append(get_warning_client_data(warning))
    return new_warning


@router.get(
    "/community/warnings/{community_patron}/paginated/{page}/{page_size}",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(verify_user_access_token)],
    summary="Warnings",
    description="Get all community warnings by pagination",
)
async def get_all_community_warnings_by_pagination(
    community_patron: str,
    page: int = 1,
    page_size: int = 100,
    user: dict = Depends(verify_user_access_token),
):
    community = await community_crud.get_community_by_patron(community_patron)

    warnings = await warning_crud.get_warnings_by_community_id_from_pagination(
        community.id, page, page_size
    )
    warnings = [get_warning_client_data(warning) for warning in warnings]
    return warnings


@router.get(
    "/community/warning/{warning_id}",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(verify_user_access_token)],
    summary="Warnings",
    description="Get warning by id",
)
async def get_community_warning(
    warning_id: str | None = None,
    user: dict = Depends(verify_user_access_token),
):
    # if warning_id == None: raise bad_request(f"No warning was send")
    user = await user_crud.get_user_by_cpf(user["cpf"])
    warning = await warning_crud.get_warning_by_id(warning_id)
    # if user.community_id != warning.community_id: raise not_found("Warning not found")
    return get_warning_client_data(warning)


@router.post(
    "/community/warnings",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(verify_user_access_token)],
    summary="Warnings",
    description="Create a warning",
)
async def create_community_warning(
    warning: CreateWarningModel, user: dict = Depends(verify_user_access_token)
):
    # if is_parish_leader(user['position']) or is_council_member(user['position']):
    user = await user_crud.get_user_by_cpf(user["cpf"])
    warning = dict(warning)
    warning["posted_by"] = user.name
    WarningValidator(warning)
    warning["community_id"] = user.community_id
    warning = await create_warning(warning)
    warning = await warning_crud.create_warning(warning)
    users = True
    page = 1
    message = MessageNotification(
        title="E-Igreja",
        body="Novo aviso postado na comunidade! Venha conferir.",
    )
    '''while users:
        users = await community_crud.get_all_community_users_paginated(
            warning.community_id, page
        )
        for user in users:
            await send_notification_to_user(user.id, message)
        page += 1'''
    return get_warning_client_data(warning)
    # raise unauthorized(f"You can't create a warning")


@router.put(
    "/community/warnings/{warning_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(verify_user_access_token)],
    summary="Warnings",
    description="Update a warning by id",
)
async def update_community_warning(
    warning: UpdateWarningModel,
    warning_id: str,
    user: dict = Depends(verify_user_access_token),
):
    # if is_parish_leader(user['position']) or is_council_member(user['position']):
    warning = dict(warning)
    warning["id"] = warning_id
    WarningValidator(warning)
    user = await user_crud.get_user_by_cpf(user["cpf"])
    warning["posted_by"] = user.name
    db_warning = await warning_crud.get_warning_by_id(warning["id"])
    # if user.community_id == db_warning.community_id:
    warning = await warning_crud.update_warning(warning)
    return get_warning_client_data(warning)
    # raise unauthorized(f"You can't update this warning")


@router.delete(
    "/community/warnings/{warning_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(verify_user_access_token)],
    summary="Warnings",
    description="Delete a warning by id",
)
async def delete_community_warning(
    warning_id: str, user: dict = Depends(verify_user_access_token)
):
    # if is_parish_leader(user['position']) or is_council_member(user['position']):
    user = await user_crud.get_user_by_cpf(user["cpf"])
    warning = await warning_crud.get_warning_by_id(warning_id)
    # if user.community_id == warning.community_id:
    return await warning_crud.delete_warning(warning)
    # raise unauthorized(f"You can't delete this warning")
