from jose import jwt, ExpiredSignatureError
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from os import getenv
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from typing import Annotated
from controller.crud.user import UserCrud
from database.session import session
from controller.errors.crud_error import CrudError

load_dotenv()

SECRET_KEY = getenv('SECRET_KEY')
ALGORITHM = getenv('ALGORITHM')
EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="signin")
user_crud = UserCrud()

def create_access_token(cpf: str, position: str = None):
    expire = datetime.now(timezone.utc) + timedelta(minutes=EXPIRE_MINUTES)
    jwt_data = {"sub_cpf": cpf, "sub_position": position, "exp": expire}
    encoded_jwt = jwt.encode(jwt_data, key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
    try:
        payload = jwt.decode(token, key=SECRET_KEY, algorithms=ALGORITHM)
        cpf = payload.get("sub_cpf")
        position = payload.get("sub_position")
        return {"cpf": cpf, "position": position}
    except:
        raise ExpiredSignatureError

async def get_user(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
    payload = decode_token(token)
    user = await user_crud.get_user_by_cpf(session, payload['cpf'])
    return dict(user)