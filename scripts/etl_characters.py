import requests
import pandas as pd
from pymongo import MongoClient

client = MongoClient('mongodb://127.0.0.1:27017/?serverSelectionTimeoutMS=2000&connectTimeoutMS=10000')
db = client['rickandmortydb']
character_collection = db['character']


url = 'https://rickandmortyapi.com/api/character/?page='

def request_principal(url, i):
    response = requests.get(url + f'{i}')
    return response.json()

def response_json(response):
    characters = []
    for value in response['results']:
        character = {
            'id' : value['id'],
            'name' : value['name'],
            'status' : value['status'],
            'species' : value['species'],
            'gender' : value['gender'],
            'origin' : value['origin'],
            'location' : value['location'],
            'url' : value['url'],
            'created' : value['created']
        }
        characters.append(character)
    return characters

lista_response = []
for i in range(1, 43):
    lista_response.extend(response_json(request_principal(url, i)))

# Insere os personagens no banco de dados
character_collection.insert_many(lista_response)

# Fecha a conexão com o banco de dados
client.close()