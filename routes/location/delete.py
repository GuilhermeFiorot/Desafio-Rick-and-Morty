from flask import request, jsonify
from utils.logger import getLoggerAplication
from middlewares.mdw_auth import auth_is_necessary
from databases import db

log = getLoggerAplication("Create Location Route")

def deleteLocation(app):
    
    @app.route("/delete_location/<int:id>", methods=["DELETE"])
    # Essa rota espera receber através de uma requisição DELETE e id (int) na url
    # e retorna os dados da location delatada
    @auth_is_necessary()
    def delete_loc(id):
        # Verificando se id existe no banco
        location_exist = db.location.find_one({"id":id})
        if not location_exist:
            return jsonify(message="Bad Request: id not found in the db.", data=[], status_code=400)
        
        # Removendo location
        db.location.delete_one({"id":id})
        
        # Atualizando location para unknow
        db.character.update_many({"locations.url": location_exist["url"]},{"$set": {"locations.$.name": "unknow", "locations.$.url": ""}})
        
        data = {
                "id": location_exist["id"],
                "name": location_exist["name"],
                "dimension": location_exist[""],
                "residents": location_exist["residents"],
                "url": location_exist["url"],
                "created": location_exist["created"]
        }
        
        return jsonify(message="Success: location deleted.", data=[{"data": data}], status_code=201)