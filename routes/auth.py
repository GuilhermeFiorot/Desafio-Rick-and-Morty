from flask import request
from utils.response_api import ResponseJsonApi
from utils.jwt_factory import generateJwt, responseJsonJwt
from middlewares.mdw_auth import auth_is_necessary


def Autenticacao(app):

    @app.route("/auth", methods=['POST'])
    def auth():
        response = request.get_json()

        # Pega os valores nas chaves do json.
        login = request.get_json().get("login")
        password = request.get_json().get("password")
        
        # Valida se tem o body passado no post.
        if response == None:
            return ResponseJsonApi({"error": "Body nessario para requisição."}, 403)

        # Gera o token.
        token_jwt, msg = generateJwt(login)

        # Verifica se o token foi gerado.
        if not token_jwt:
            return ResponseJsonApi({"error": str(msg)}, 403)

        # Pega a mensagem para retornar para API, com as informação de autenticação.
        response_jwt = responseJsonJwt(token_jwt)

        # Retorna na API as informações e status code 200, sucesso.
        return ResponseJsonApi(response_jwt, 200)

    @app.route("/isauth")
    @auth_is_necessary()
    def isauth():
        return ResponseJsonApi({"ok": True},200)
