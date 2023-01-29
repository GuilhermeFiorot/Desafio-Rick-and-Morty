from flask import request, jsonify
from utils.logger import getLoggerAplication
from middlewares.mdw_auth import auth_is_necessary
from databases import db
from utils.char_validations import gender_valid, status_valid, origin_valid, location_valid

log = getLoggerAplication("Update Character Route")

def updateCharacter(app):
    
    @app.route("/update_character/<int:id>", methods=['PUT'])
    # Essa rota espera receber através de uma requisição PUT, id (int) na url e formato Json pelo menos um dos dados a seguir:
    # name, status(Alive, Dead ou Unknow), species, gender(Male, Female, Genderless ou unknow), origin(nome ou unknow) e location(nome ou unknow)
    # e retorna os dados do personagem atualizado
    @auth_is_necessary()
    def update_char(id):
        character_exist = db.character.find_one({"id":id})
        if not character_exist:
            return jsonify(message='Bad Request: id dont exist.', data=[],status_code=201)
        
        response = request.get_json()
        
        validations = {
            'status': (status_valid, "Bad Request : status value not in [Dead, Alive, unknow]."),
            'gender': (gender_valid, "Bad Request : gender value not in [Male, Female, Genderless, unknow]."),
        }
        origin_url = ""
        location_url = ""
        for key in response.keys():
            if key in validations:
                validation_func, error_msg = validations[key]
                if not validation_func(response.get(key)):
                    return jsonify(message=error_msg, status_code=400)
            
            if key == "location":
                if response.get(key) != "unknow":
                    location_url = location_valid(response.get(key))
                    if not location_url:
                        return jsonify(message="Bad Request : location name dont exist in db.", status_code=400)
            elif key == "origin":
                if response.get(key) != "unknow":
                    origin_url = origin_valid(response.get(key))
                    if not origin_url:
                        return jsonify(message="Bad Request : origin name dont exist in db.", status_code=400)
            
            if response.get(key) == "":
                return jsonify(message=f'Bad Request: {key} value is invalid.', data=[], status_code=400)
        
        db.character.update_one(response)
        
        return jsonify(message='Success: character updated', data=[{"data": response}], status_code=201)