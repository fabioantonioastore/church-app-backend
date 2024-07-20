from models.login import Login
from uuid import uuid4
from controller.auth.password import hash_pasword, verify_hashed_password
from controller.crud.login import LoginCrud
from database.session import session
from controller.auth.cpf_hash import hash_cpf

login_crud = LoginCrud()

def create_login(login_data: dict) -> Login:
    login = Login()
    for key in login_data.keys():
        match key:
            case "cpf":
                login.cpf = hash_cpf(login_data['cpf'])
            case "position":
                login.position = login_data['position']
            case "password":
                login.password = hash_pasword(login_data['password'])
    login.id = str(uuid4())
    return login

async def verify_user_login(login_data: dict) -> bool:
    login = await login_crud.get_login_by_cpf(session, hash_cpf(login_data['cpf']))
    return verify_hashed_password(login_data['password'], login.password)

async def verify_admin_login(login_data: dict) -> bool:
    login = await login_crud.get_login_by_cpf(session, hash_cpf(login_data['cpf']))
    if login.position:
        if login.position == login_data['position']:
            return verify_hashed_password(login_data['password'], login.password)
    return False