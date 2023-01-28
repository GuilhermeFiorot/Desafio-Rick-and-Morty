from flask import request, jsonify
from utils.logger import getLoggerAplication
from middlewares.mdw_auth import auth_is_necessary
from databases import db
from datetime import datetime
from utils.char_validations import validate_create, char_exists

log = getLoggerAplication("Create Character Route")

def createCharacter(app):
    
    @app.route("/create_character", methods=["POST"])
    @auth_is_necessary()
    def create_char():
        name = request.get_json().get("name")
        status = request.get_json().get("status")
        species = request.get_json().get("species")
        gender = request.get_json().get("gender")
        origin = request.get_json().get("origin")
        location = request.get_json().get("location")

        try:
            validate_create(name, status, species, gender, origin, location)
            # rest of the code
        except ValueError as e:
            return jsonify(message=str(e), status_code=400)
        
        location_url = ""
        origin_url = ""
        if origin != 'unknow':
            origin_url = db.location.find_one({"name":origin},{"url":1, "_id":0})["url"]
        if location != 'unknow':
            location_url = db.location.find_one({"name":location},{"url":1, "_id":0})["url"]
        
        if char_exists(name, status, species, gender, origin, origin_url, location, location_url):
            return jsonify(message="Bad Request: character already exist in db.", status_code=400)
        
        last_id = db.character.find({},{"id":1,"_id":0}).sort("_id", -1).limit(1)
        id = int(last_id[0].get("id"))+1
        data = {
                "id": id,
                "name": name,
                "status": status,
                "species": species,
                "gender": gender,
                "origin": [origin, origin_url],
                "location": [location, location_url],
                "url": f"https://rickandmortyapi.com/api/character/{id}",
                "created": datetime.now().isoformat()
        }
        db.character.insert_one(data)
        return jsonify(message="Success: character created.", data={"data":data}, status_code=201)