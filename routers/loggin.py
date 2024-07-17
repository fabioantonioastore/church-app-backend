from fastapi import APIRouter
from schemas.sign import SignIn, SignUp
from controller.validators.sign_validator import SignValidator

router = APIRouter()

@router.post("/signin")
async def signin():
    pass

@router.post("/signup")
async def signup(sign_data: SignUp):
    sign_data = dict(sign_data)
    SignValidator(sign_data)