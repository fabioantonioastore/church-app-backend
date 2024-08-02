from models.user import User
from models.payment import Payment
from uuid import uuid4
from datetime import datetime
from controller.crud.community import CommunityCrud
from database.session import session
from controller.auth.cpf_cryptography import get_crypted_cpf, get_plain_cpf
from models.login import Login
from controller.src.login import upgrade_login_position
from typing import NamedTuple
from controller.validators.date import DateValidator
from controller.validators.cpf import CPFValidator
from controller.validators.email import EmailValidator
from controller.validators.password import PasswordValidator
from controller.crud.login import LoginCrud
from controller.auth.password import hash_pasword

community_crud = CommunityCrud()
login_crud = LoginCrud()

async def get_community_id(community_patron: str) -> str:
    community = await community_crud.get_community_by_patron(session, community_patron)
    return community.id

async def create_user(user_data: dict) -> User:
    user = User()
    for key in user_data.keys():
        match key:
            case "name":
                user.name = user_data['name']
            case "cpf":
                user.cpf = get_crypted_cpf(user_data['cpf'])
            case "position":
                user.position = user_data['position']
            case "birthday":
                user.birthday = datetime.strptime(user_data['birthday'], "%Y-%m-%d")
            case "email":
                user.email = user_data['email']
            case "image":
                user.image = user_data['image']
            case "community":
                user_data['community'] = await get_community_id(user_data['community'])
                user.community_id = user_data['community']
    user.id = str(uuid4())
    return user

async def get_community_patron(community_id: str) -> str:
    community = await community_crud.get_community_by_id(session, community_id)
    return community.patron

async def get_user_client_data(user: User) -> dict:
    user_data = {}
    user_data['name'] = user.name
    user_data['birthday'] = user.birthday
    user_data['position'] = user.position
    user_data['image'] = user.image
    user_data['community'] = await get_community_patron(user.community_id)
    user_data['email'] = user.email
    user_data['cpf'] = get_plain_cpf(user.cpf)

    return user_data

async def is_council_member(position: str) -> bool:
    return position == "council member"

async def is_parish_leader(position: str) -> bool:
    return position == "parish leader"

def convert_user_to_dict(user: User) -> dict:
    new_user = {'id': user.id, 'name': user.name, 'image': user.image, 'position': user.position,
                'community_id': user.community_id, 'birthday': user.birthday, 'cpf': user.cpf, 'email': user.email,
                'active': user.active}
    return new_user

def upgrade_user_position(user: User, login: Login, position: str):
    class Data(NamedTuple):
        user: dict
        login: dict

    user = convert_user_to_dict(user)
    user['position'] = position
    login = upgrade_login_position(login, position)

    return Data(user=user, login=login)

async def get_update_data(user: User, update_data: dict) -> dict:
    print(update_data)
    for key in update_data:
        match key:
            case "name":
                if update_data['name'] != None:
                    user.name = update_data['name']
            case "birthday":
                if update_data['birthday'] != None:
                    DateValidator(update_data['birthday'])
                    user.birthday = datetime.strptime(update_data['birthday'], "%Y-%m-%d")
            case "cpf":
                if update_data['cpf'] != None:
                    CPFValidator(update_data['cpf'])
                    user.cpf = get_crypted_cpf(update_data['cpf'])
            case "email":
                if update_data['email'] != None:
                    EmailValidator(update_data['email'])
                    user.email = update_data['email']
            case "password":
                if update_data['password'] != None:
                    PasswordValidator(update_data['password'])
                    login = await login_crud.get_login_by_cpf(session, get_crypted_cpf(user.cpf))
                    login.password = hash_pasword(update_data['password'])
                    await login_crud.update_login(session, login)
            case "community":
                if update_data['community'] != None:
                    community = await community_crud.get_community_by_patron(session, update_data['community'])
                    user.community_id = community.id
        return convert_user_to_dict(user)