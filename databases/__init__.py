from pymongo import MongoClient

# Configurações de Banco de Dados
uri = 'mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.6.2'
client = MongoClient(uri)
db = client['rickandmortydb']