from flask import request, jsonify
from utils.logger import getLoggerAplication
from middlewares.mdw_auth import auth_is_necessary
from databases import db

log = getLoggerAplication("Update Location Route")

def updateLocation(app):
    
    @app.route("/update_location/<int:id>", methods=['PUT'])
    @auth_is_necessary()
    def update_loc(id):
        location_exist = db.location.find_one({"id":id})
        if not location_exist:
            return jsonify(message='Bad Request: id dont exist.', data=[],status_code=201)
        
        response = request.get_json()
        
        for key in response.keys():
            if key == 'name':
                name = response.get(key)
                if name == "":
                    return jsonify(message='Bad Request: name is empty.', data=[],status_code=201)
                else:
                    name_exist = db.location.find_one({"name": name})
                    if name_exist:
                        return jsonify(message='Bad Request: name already exist.', data=[],status_code=201)
            elif key == "dimension":
                dimension = response.get(key)
                if dimension == "":
                    response[key] = "unknow"
                    
        db.location.update_one(response)
        
        return jsonify(message='Success: location updated', data=[{"data": response}], status_code=201)