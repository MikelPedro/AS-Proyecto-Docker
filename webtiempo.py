from flask import Flask, render_template, request, flash
from tiempo import main as get_datosTiempo
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, OperationFailure
import os

app = Flask(__name__, template_folder='./app')
app.config['SECRET_KEY'] = 'SecretoLlave' # esto es para le flash
URL_ORIGINAL = "https://api.openweathermap.org/data/2.5/weather?id="
API_KEY = open('api_key','r').read()


mongo_uri = "mongodb://root:example@mongo:27017/mydatabase?authSource=admin"  # Reemplaza con tu propia URI si es necesario

# Conectarse a la base de datos
client = MongoClient(mongo_uri)
db = client.mydatabase


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
            else:

                datos = {
                    'lugar': datosTiempo.lugar,
                    'tempAct': datosTiempo.tempAct,
                    'tempMin': datosTiempo.tempMin,
                    'tempMax': datosTiempo.tempMax,
                    'humedad': datosTiempo.humedad,
                    'descrip': datosTiempo.descrip,
                    'icono': datosTiempo.icono,
                    'fecha': datetime.now()  # Añadir la fecha actual
                }

                db.ciudades.insert_one(datos)
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

    lista = db.ciudades.find()

    #cities_data = list(db.ciudades.find())
    return render_template('cities.html', data=lista)


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=3000, debug=True)
