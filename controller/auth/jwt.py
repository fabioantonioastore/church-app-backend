from jose import jwt, ExpiredSignatureError
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from os import getenv
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from typing import Annotated

load_dotenv()

SECRET_KEY = getenv('SECRET_KEY')
ALGORITHM = getenv('ALGORITHM')
EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="signin")
def create_access_token(cpf: str, position: str = None):
    expire = datetime.now(timezone.utc) + timedelta(minutes=EXPIRE_MINUTES)
    jwt_data = {"sub_cpf": cpf, "sub_position": position, "exp": expire}
    encoded_jwt = jwt.encode(jwt_data, key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, key=SECRET_KEY, algorithms=ALGORITHM)
        cpf = payload.get("sub_cpf")
        position = payload.get("sub_position")
        return {"cpf": cpf, "position": position}
    except:
        raise ExpiredSignatureError