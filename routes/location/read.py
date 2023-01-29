from flask import request, jsonify
from utils.logger import getLoggerAplication
from middlewares.mdw_auth import auth_is_necessary
from databases import db

log = getLoggerAplication("Read Location Route")

def readLocation(app):
    @app.route("/read_location", methods=["GET"])
    # Essa rota espera receber através de uma requisição GET e formato Query o dado:
    # Page (int)
    # e retorna os dados das locations de forma paginada (10 por pagina)
    @auth_is_necessary()
    def read_loc():
        page = request.args.get("page", 1, type=int)
        locations = db.location.aggregate([
                                            {
                                                "$skip": (page - 1) * 10
                                            },
                                            {
                                                "$limit": 10
                                            }
                                            ])
        data = []
        for location in locations:
            data.append({
                	"id": location["id"],
                    "name": location["name"],
                    "dimension": location["dimension"],
                    "residents": location["residents"],
                    "url": location["url"],
                    "created": location["created"]
            })
        count = db.location.count_documents({})
        info = {
            "count": count,
            "pages": count // 10,
            "next": f"{request.base_url}?page={page + 1}" if page < count / 10 else None,
            "prev": f"{request.base_url}?page={page - 1}" if page > 1 else None
        }
        
        return jsonify(message="Success", data=[{"info": info, "data": data}], status_code=201)
    
    @app.route("/read_location/<int:id>", methods=['GET'])
    # Essa rota espera receber através de uma requisição GET e id (int) na url
    # e retorna os dados da location de forma unica pelo id
    @auth_is_necessary()
    def read_locId(id):
        location_exist = db.location.find_one({"id": id})
        if location_exist:
            data = {
                    "id": location_exist["id"],
                    "name": location_exist["name"],
                    "dimension": location_exist["dimension"],
                    "residents": location_exist["residents"],
                    "url": location_exist["url"],
                    "created": location_exist["created"]
            }
        else:
            return jsonify(message="Bad Request: id not found in db.", data=[], status_code=201)    
        return jsonify(message="Success", data={"data": data}, status_code=201)