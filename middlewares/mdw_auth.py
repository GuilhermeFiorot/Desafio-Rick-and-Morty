from functools import wraps
from flask import request
from utils.response_api import ResponseJsonApi
from utils.jwt_factory import validateJwt
from utils.logger import getLoggerAplication

log = getLoggerAplication("Middle Auth")

def auth_is_necessary():
    def _auth_is_necessary(f):
        @wraps(f)
        def __auth_is_necessary(*args, **kwargs):

            log.debug("Verificando usuário autenticado...")

            # Pega o header Autorization.
            headerAuth = request.headers.get("Authorization")

            # Verifica se foi passado, se não retornar informando que não esta autorizado.
            if not headerAuth:
                return ResponseJsonApi({"error" : "Header de Autorização necessario."}, 401)

            # Separa o prefixo do token para verificar se ambos sao validos.
            prefix_token = headerAuth.split(" ")

            # Verifica se ah somente o prefixo e o token
            if len(prefix_token) != 2:
                return ResponseJsonApi({"error" : "Token mal formatado, verifique se esta no padrão correto."}, 401)

            log.debug("Pegando o prefixo do token!")

            # Pega o prefixo.
            prefixo = prefix_token[0]

            # Verifica se o prefixo e o padrao valido.
            if prefixo != "Bearer":
                return ResponseJsonApi({"error" : "Token mal formatado, prefixo invalido."}, 401)

            # Pega o token
            token_jwt = prefix_token[1]

            log.debug("Validando o token!")

            # Valida o JWT informado na rota.
            token_jwt, msg = validateJwt(token_jwt)

            # Verifica se o JWT esta
            if not token_jwt:
                return ResponseJsonApi({"error" : str(msg)}, 401)
            
            log.debug("Token está valido!")

            return f(*args, **kwargs)
        return __auth_is_necessary
    return _auth_is_necessary