from fastapi import HTTPException, status

def not_found(message: str = None):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

def bad_request(message: str = None):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)

def unauthorized(message: str = None):
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=message)

def payment_required(message: str = None):
    raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED, detail=message)

def forbidden(message: str = None):
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=message)

def method_not_allowed(message: str = None):
    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail=message)

def not_acceptable(message: str = None):
    raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=message)

def request_timeout(message: str = None):
    raise HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT, detail=message)

def unsupported_media_type(message: str = None):
    raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail=message)

def im_a_teapot(message: str = None):
    raise HTTPException(status_code=status.HTTP_418_IM_A_TEAPOT, detail=message)

def unprocessable_content(message: str = None):
    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=message)

def locked(message: str = None):
    raise HTTPException(status_code=status.HTTP_423_LOCKED, detail=message)

def failed_dependency(message: str = None):
    raise HTTPException(status_code=status.HTTP_424_FAILED_DEPENDENCY, detail=message)

def too_early(message: str = None):
    raise HTTPException(status_code=status.HTTP_425_TOO_EARLY, detail=message)

def precondition_required(message: str = None):
    raise HTTPException(status_code=status.HTTP_428_PRECONDITION_REQUIRED, detail=message)
def too_many_requests(message: str = None):
    raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail=message)

def internal_server_error(message: str = None):
    raise HTTPException(status_code=status.WS_1011_INTERNAL_ERROR, detail=message)

def not_implemented(message: str = None):
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=message)

def bad_gateway(messsage: str = None):
    raise HTTPException(status_code=status.WS_1014_BAD_GATEWAY, detail=messsage)

def service_unavailable(message: str = None):
    raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=message)

def gateway_timeout(message: str = None):
    raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT, detail=message)

def http_version_not_supported(message: str = None):
    raise HTTPException(status_code=status.HTTP_505_HTTP_VERSION_NOT_SUPPORTED, detail=message)

def loop_detected(messasge: str = None):
    raise HTTPException(status_code=status.HTTP_508_LOOP_DETECTED, detail=messasge)

def network_authentication_required(message: str = None):
    raise HTTPException(status_code=status.HTTP_511_NETWORK_AUTHENTICATION_REQUIRED, detail=message)