# Importando librarys necessarias
from flask import Flask
from flask_cors import CORS

# Importando rotas auxiliares
from routes import auth, error
from utils.logger import settingsColor
# Importando rotas character
from routes.character.create import createCharacter
from routes.character.read import readCharacter
from routes.character.update import updateCharacter
from routes.character.delete import deleteCharacter
# Importando rotas location
from routes.location.create import createLocation
from routes.location.read import readLocation
from routes.location.update import updateLocation
from routes.location.delete import deleteLocation

# Configurações para o Inicializar o App
app = Flask(__name__)
CORS(app)
# Configurações extras
settingsColor() # Configuração de cores dos logs do terminal

# Rotas Auxiliares
auth.Autenticacao(app)
error.Error(app)
# Rotas para CRUD Character
createCharacter(app)
readCharacter(app)
updateCharacter(app)
deleteCharacter(app)
# Rotas para CRUD Location
createLocation(app)
readLocation(app)
updateLocation(app)
deleteLocation(app)

if __name__ == "__main__":
    app.run( host = '0.0.0.0', debug=True)