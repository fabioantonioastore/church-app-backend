from fastapi import Request
from controller.auth import jwt


async def verify_user_access_token(request: Request) -> dict:
    access_token = request.headers.get("Authorization")
    user = jwt.decode_token(access_token)
    return user
