from databases import db

def char_exists(name, status, species, gender, origin, origin_url, location, location_url):
    # Verifica se ja existe um registro igual no banco
    char_exist = db.character.find_one({"name":name, "status":status, "species":species, "gender":gender, "origin": [origin, origin_url], "location": [location, location_url]})
    if char_exist:
        return True
    return False

def origin_valid(origin):
    # Verifica se a origin existe
    origin_exist = db.location.find_one({"name":origin})
    if not origin_exist:
        return False
    return True

def location_valid(location):
    # Verifica se a location existe
    if location == 'unknow':
        return True    
    location_exist = db.location.find_one({"name":location})
    if not location_exist:
        return False
    return True

def status_valid(status):
    # Verifica classificacao de status
    if status not in ["Alive", "Dead", "unknown"]:
        return False
    return True

def gender_valid(gender):
    # Verifica classificacao de genero
    if gender not in ["Male", "Female", "Genderless", "unknow"]:
        return False
    return True

def validate_create(name, status, species, gender, origin, location):
    # Verifica se existe alguma entrada vazia e suas respectivas validacoes
    if not all([name, status, species, gender, origin, location]):
        raise ValueError("Bad Request : empty value in payload.")
    if not status_valid(status):
        raise ValueError("Bad Request : status value not in [Dead, Alive, unknow].")
    if not gender_valid(gender):
        raise ValueError("Bad Request : gender value not in [Male, Female, Genderless, unknow].")
    if not location_valid(location):
        raise ValueError("Bad Request : location name dont exist in db.")
    if not origin_valid(origin):
        raise ValueError("Bad Request : origin name dont exist in db.")