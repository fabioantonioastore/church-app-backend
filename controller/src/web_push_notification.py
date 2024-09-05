from models.web_push import WebPush


def create_web_push_model(web_push_data: dict) -> WebPush:
    web_push = WebPush()
    web_push.endpoint = web_push_data["endpoint"]
    web_push.p256dh = web_push_data["p256dh"]
    web_push.auth = web_push_data["auth"]
    web_push.user_id = web_push_data["user_id"]
    return web_push
