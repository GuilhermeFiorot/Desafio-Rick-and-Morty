from flask import request, jsonify
from utils.logger import getLoggerAplication
from middlewares.mdw_auth import auth_is_necessary
from databases import db

log = getLoggerAplication("Delete Character Route")

def deleteCharacter(app):
    
    @app.route("/delete_character/<int:id>", methods=['DELETE'])
    # Essa rota espera receber através de uma requisição DELETE e id indentificado na url
    # Apaga os dados do usuario e apaga usuario da lista de residents na tabela location
    # e retorna os dados do personagem apagado
    @auth_is_necessary()
    def delete_char(id):
        # Verificando se id existe no banco
        char_exist = db.character.find_one({"id":id})
        if not char_exist:
            return jsonify(message='Bad Request: id not found in the db.', data=[], status_code=400)
        
        # Deletando da colecao character
        db.character.delete_one({"id":id})
        # Removendo URL do local que ele reside
        db.location.update_many({}, {"$pull": {"residents": char_exist['url']}})
        
        data = {
                "id": id,
                "name": char_exist["name"],
                "status": char_exist["status"],
                "species": char_exist["species"],
                "gender": char_exist["gender"],
                "origin": char_exist["origin"],
                "location": char_exist["location"],
                "url": char_exist["url"],
                "created": char_exist["created"]
        }
        
        return jsonify(message="Success: character deleted.", data=[{"data": data}], status_code=201)