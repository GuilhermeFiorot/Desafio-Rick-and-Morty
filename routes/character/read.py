from flask import request, jsonify
from utils.logger import getLoggerAplication
from middlewares.mdw_auth import auth_is_necessary
from databases import db

log = getLoggerAplication("Read Character Route")

def readCharacter(app):
    
    @app.route("/read_character", methods=['GET'])
    # Essa rota espera receber através de uma requisição GET e formato Query o dado:
    # Page (int)
    # e retorna os dados dos personagens de forma paginada (10 por pagina)
    @auth_is_necessary()
    def read_char():
        page = request.args.get("page", 1, type=int)
        characters = db.character.aggregate([
                                            {
                                                "$skip": (page - 1) * 10
                                            },
                                            {
                                                "$limit": 10
                                            }
                                            ])
        data = []
        for character in characters:
            data.append({
                	"id": character["id"],
                    "name": character["name"],
                    "status": character["status"],
                    "species": character["species"],
                    "gender": character["gender"],
                    "origin": character["origin"],
                    "location": character["location"],
                    "url": character["url"],
                    "created": character["created"]
            })
        count = db.character.count_documents({})
        info = {
            "count": count,
            "pages": count // 10,
            "next": f"{request.base_url}?page={page + 1}" if page < count / 10 else None,
            "prev": f"{request.base_url}?page={page - 1}" if page > 1 else None
        }
        
        return jsonify(message="Success", data={"info": info, "data": data}, status_code=201)
    
    @app.route("/read_character/<int:id>", methods=['GET'])
    # Essa rota espera receber através de uma requisição GET e id (int) na url
    # e retorna os dados do personagem de forma unica pelo id
    @auth_is_necessary()
    def read_charId(id):
        character_exist = db.character.find_one({"id": id})
        if character_exist:
            data = {
                    "id": character_exist["id"],
                    "name": character_exist["name"],
                    "status": character_exist["status"],
                    "species": character_exist["species"],
                    "gender": character_exist["gender"],
                    "origin": character_exist["origin"],
                    "location": character_exist["location"],
                    "url": character_exist["url"],
                    "created": character_exist["created"]
            }
        else:
            return jsonify(message="Bad Request: id not found in db.", data=[], status_code=400)
        return jsonify(message="Success", data={"data": data}, status_code=201)