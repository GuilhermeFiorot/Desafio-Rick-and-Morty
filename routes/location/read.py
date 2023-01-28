from flask import request, jsonify
from utils.logger import getLoggerAplication
from middlewares.mdw_auth import auth_is_necessary
from databases import db

log = getLoggerAplication("Read Location Route")

def readLocation(app):
    @app.route("/read_location", methods=["GET"])
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
            print(location)
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
    @auth_is_necessary()
    def read_locId(id):
        location = db.location.find_one({"id": id})
        data = {
                "id": location["id"],
                "name": location["name"],
                "dimension": location["dimension"],
                "residents": location["residents"],
                "url": location["url"],
                "created": location["created"]
        }
        
        return jsonify(message="Success", data={"data": data}, status_code=201)