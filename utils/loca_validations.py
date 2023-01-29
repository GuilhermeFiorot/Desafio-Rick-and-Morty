from databases import db

def loca_exist(name, dimension):
    # Verifica se ja existe um registro igual no banco
    location_exist = db.location.find_one({'name':name, 'dimension':dimension})
    if location_exist:
        return True
    return False

def validate_residents(residents):
    if len(residents) > 0:
        # Verifica se ja existe um registro igual no banco
        residents_exist = db.character.find({'names': {"$all": residents}})
        if residents_exist.count() == len(residents):
            return True
        return False
    return True

def validate_loca(name, dimension, residents):
    # Verifica se existe alguma entrada vazia
    if not all([name, dimension]):
        raise ValueError("Bad Request : empty value in payload.")
    if not validate_residents(residents):
        raise ValueError("Bad Request: residents dont exist in db.")