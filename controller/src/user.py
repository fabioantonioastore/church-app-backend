from models.user import User
from models.payment import Payment
from uuid import uuid4
from datetime import datetime
from controller.crud.community import CommunityCrud
from database.session import session
from controller.auth.cpf_cryptography import get_crypted_cpf, get_plain_cpf

community_crud = CommunityCrud()

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