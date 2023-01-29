from flask import request, jsonify
from utils.logger import getLoggerAplication
from middlewares.mdw_auth import auth_is_necessary
from databases import db
from datetime import datetime
from utils.loca_validations import validate_loca, loca_exist

log = getLoggerAplication("Create Location Route")

def createLocation(app):
    
    @app.route("/create_location", methods=['POST'])
    @auth_is_necessary()
    def create_loca():
        name = request.get_json().get("name")
        dimension = request.get_json().get("dimension")
        residents = request.get_json().get("residents")

        try:
            validate_loca(name, dimension, residents)
        except ValueError as e:
            return jsonify(message=str(e), status_code=400)
        
        if loca_exist(name, dimension):
            return jsonify(message="Bad Request: location already exist in db.", status_code=400)
        
        resident_list = []            
        if len(residents) > 0:
            resident_exist = db.character.find({'names': {"$all": residents}})
            for resident in resident_exist:
                resident_list.append(resident["url"])
        
        last_id = db.location.find({},{"id":1,"_id":0}).sort("_id", -1).limit(1)
        id = int(last_id[0].get("id"))+1
        data = {
                "id": id,
                "name": name,
                "dimension": dimension,
                "residents": resident_list,
                "url": f"https://rickandmortyapi.com/api/character/{id}",
                "created": datetime.now().isoformat()
        }
        db.character.insert_one(data)
        return jsonify(message="Success: location created.", data={"data":data}, status_code=201)