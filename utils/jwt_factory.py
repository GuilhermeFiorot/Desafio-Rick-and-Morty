import jwt
from datetime import datetime, timedelta, timezone
from utils.logger import getLoggerAplication

JWT_SECRET = "$2a$12$oiNkj.Qk6Y6KCYmA2eVIZOT0aK1TFKIb3ype4fya/ZqpUJzVwhYqG"
TIME_HOUR_EXPIRATION = 1

log = getLoggerAplication("jwt_factory")

def __message_jwt(payload):
    return {
        'sub': payload,
        'exp': datetime.now(timezone.utc) + timedelta(hours=TIME_HOUR_EXPIRATION),
    }

def responseJsonJwt(jwt):
    return {
        "auth_token" : jwt,
        "prefix" : "Bearer",
        "header" : "Authorization"
    }

def generateJwt(payload):
    try:
        MESSAGE = __message_jwt(payload)
        token = jwt.encode(MESSAGE, JWT_SECRET, algorithm="HS256")
        return [token, '']
    except Exception as e:
        log.error("Erro ao gerar o Token Jwt")
        log.error(e)
        return [None, e]


def validateJwt(token):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return [payload, '']
    except Exception as e:
        log.error("Erro ao validar o Token Jwt")
        log.error(e)
        return [None, e]

def responseJsonJwt(jwt):
    return {
        "auth_token" : jwt,
        "prefix" : "Bearer",
        "header" : "Authorization"
    }