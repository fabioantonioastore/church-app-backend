from models.user import User
from models.payment import Payment
from uuid import uuid4
from datetime import datetime
from controller.auth.cpf_hash import hash_cpf

def create_user(user_data: dict) -> User:
    user = User()
    for key in user_data.keys():
        match key:
            case "name":
                user.name = user_data['name']
            case "cpf":
                user.cpf = hash_cpf(user_data['cpf'])
            case "position":
                user.position = user_data['position']
            case "birthday":
                user.birthday = datetime.strptime(user_data['birthday'], "%Y/%m/%d")
            case "email":
                user.email = user_data['email']
            case "image":
                user.image = user_data['image']
            case "community_id":
                user.community_id = user_data['community_id']
    user.id = str(uuid4())
    return user