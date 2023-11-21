from flask import Flask, render_template, request, flash
from tiempo import main as get_datosTiempo
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, OperationFailure
import os

app = Flask(__name__, template_folder='./app')
app.config['SECRET_KEY'] = 'SecretoLlave' # esto es para le flash
#app.config['MONGO_URI'] = 'mongodb://localhost:27017/test'  # Reemplaza con la URI de tu base de datos

#mongo = MongoClient(app.config['MONGO_URI'])
#client = pymongo.MongoClient(host='localhost', port=27017)
#user='root', password='pass', authSource='admin')
#client = MongoClient("mongodb://user:pass@cs_mongodb:27017/?authMechanism=DEFAULT&authSource=entrega",serverSelectionTimeoutMS=500)
#mydb = client.entrega  #Seleccionar db
#ciudades = mydb.ciudadtemp #seleccionar coleccion
#db = mongo.test
#ciudades = db.ciudades
"""
client = MongoClient(host='test_mongodb',
                         port=27017, 
                         username='root', 
                         password='pass',
                        authSource="admin")
db = client["animal_db"]


MONGO_HOST = "mongodb" 
MONGO_PORT = "27017"
MONGO_DB = "datos"
MONGO_USER = "admin"
MONGO_PASS = "pass"

uri = "mongodb://{}:{}@{}:{}/{}?authSource=admin".format(MONGO_USER, MONGO_PASS, MONGO_HOST, MONGO_PORT, MONGO_DB)
client = MongoClient(uri)
mydb = client.datos 
"""

mongodb_host = os.environ.get('MONGO_HOST', 'localhost')
mongodb_port = int(os.environ.get('MONGO_PORT', '27017'))
client = MongoClient(mongodb_host, mongodb_port)    #Configure the connection to the database
db = client.proyecto   #Select the database
ciudades = db.ciutemp #Select the collection

URL_ORIGINAL = "https://api.openweathermap.org/data/2.5/weather?id="
API_KEY = open('api_key','r').read()

#def ciudad_existe(ciudad):
    # Verifica si la ciudad ya existe en la base de datos
#    return mongo.db.ciudades.find_one({'lugar': ciudad}) is not None

@app.route('/', methods=[ 'GET', 'POST'])
def index():
    
    error_msg = ''
    datosTiempo = None
    ciudad = None
    if request.method == 'POST':
        ciudad = request.form['ciudad']
        print(f"Ciudad recibida: {ciudad}")
        #existe = mongo.db.ciudades.find_one({'lugar': datosTiempo.lugar})

        if not ciudad:
            error_msg = "Introduzca una ciudad"
            #elif ciudad_existe(ciudad):
            #    error_msg = f'La ciudad {ciudad} ya está en la base de datos'
        else:
            datosTiempo = get_datosTiempo(ciudad)
            if datosTiempo == 'Error':
                error_msg = 'Esa no es una ciudad válida!'
            # Crear un nuevo diccionario con solo los atributos que quieres insertar
            datos = {
                'lugar': datosTiempo.lugar,
                'tempAct': datosTiempo.tempAct,
                'tempMin': datosTiempo.tempMin,
                'tempMax': datosTiempo.tempMax,
                'humedad': datosTiempo.humedad,
                'descrip': datosTiempo.descrip,
                'fecha': datetime.now()  # Añadir la fecha actual
            }

            ciudades.insert_one(datos)
            print(datosTiempo)
            #db.ciudades.insert_one(datosTiempo.__dict__)

        if error_msg:
            flash(error_msg, 'error')
        else:
            flash('Ciudad añadida exitosamente!', 'success')

       
   # ciudades_guardadas = mongo.db.ciudades.find()
    return render_template('index.html', data=datosTiempo)

@app.route('/cities')
def cities():

    #lista = ciudades.find()

    #cities_data = list(db.ciudades.find())
    return render_template('cities.html')


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=3000, debug=True)
