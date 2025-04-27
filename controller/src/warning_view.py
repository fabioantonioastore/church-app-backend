from models import WarningView
from models import User
from controller.crud import WarningViewCRUD, UserCrud


warning_view_crud = WarningViewCRUD()
user_crud = UserCrud()


async def create_warning_view(warning_id: str, user: User) -> WarningView:
    warning_view = WarningView()
    warning_view.warning_id = warning_id
    warning_view.cpf = user.cpf

    return await warning_view_crud.create_warning_view(warning_view)


async def get_users_name_from_warning_id(warning_id: str) -> list[str]:
    warnings_view = await warning_view_crud.get_warnings_view_by_warning_id(warning_id)
    users_names = []

    for warning_view in warnings_view:
        user = await user_crud.get_user_by_cpf(warning_view.cpf)
        users_names.append(user.name)

    return users_names


async def get_warning_view_no_sensitive_data(
    warning_id: str, client: bool = False
) -> list[dict] | None:
    result = []

    try:
        warnings_view = await warning_view_crud.get_warnings_view_by_warning_id(
            warning_id
        )
    except:
        return result

    for warning_view in warnings_view:
        user = await user_crud.get_user_by_cpf(warning_view.cpf)

        data = dict()
        data["name"] = user.name
        data["date"] = warning_view.date
        if not client:
            data["cpf"] = user.cpf

        result.append(data)

    return result
