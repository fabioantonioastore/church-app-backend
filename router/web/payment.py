from fastapi import APIRouter, WebSocket, Depends
from routers.middleware.authorization import verify_user_access_token

router = APIRouter()

@router.websocket("/verify_pix_payment", dependencies=[Depends(verify_user_access_token)])
async def verify_pix_payment_web_socket(websocket: WebSocket, user = Depends(verify_user_access_token)):
    await websocket.accept()
    while True:
        data = await websocket.receive_json()