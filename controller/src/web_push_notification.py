from models.web_push import WebPush


def create_web_push_model(web_push_data: dict) -> WebPush:
    web_push = WebPush()
    web_push.token = web_push_data["token"]
    web_push.user_id = web_push_data["user_id"]
    return web_push
