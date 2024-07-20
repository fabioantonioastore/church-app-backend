from fastapi import FastAPI
import routers.user
import routers.community
import routers.login
from controller.auth import jwt

app = FastAPI()

app.include_router(routers.user.router)
app.include_router(routers.community.router)
app.include_router(routers.login.router)

@app.get("/")
async def root():
    access_token = jwt.create_access_token("hello@gmail.com")
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/token")
async def token_route(token: str):
    user = jwt.decode_token(token)
    return user