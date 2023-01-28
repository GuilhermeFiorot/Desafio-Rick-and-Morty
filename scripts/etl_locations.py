import requests
import pandas as pd
from pymongo import MongoClient

client = MongoClient('mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.6.2')
db = client['rickandmortydb']
location_collection = db['location']

url = 'https://rickandmortyapi.com/api/location/?page='

def request_principal(url, i):
    r = requests.get(url + f'{i}')
    return r.json()

def response_json(response):
    locations = []
    for value in response['results']:
        location = {
            'id': value['id'],
            'name' : value['name'],
            'dimension' : value['dimension'],
            'residents' : value['residents'],
            'url' : value['url'],
            'created' : value['created']
        }
        locations.append(location)
    return locations

lista_response = []
for i in range(1, 8):
    lista_response.extend(response_json(request_principal(url, i)))

# Insere os personagens no banco de dados
location_collection.insert_many(lista_response)

# Fecha a conexão com o banco de dados
client.close()