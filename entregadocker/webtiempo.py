from flask import Flask, redirect, render_template, request, flash
from tiempo import main as get_datosTiempo
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, OperationFailure
from bson import ObjectId



app = Flask(__name__, template_folder='./templates')
app.config['SECRET_KEY'] = 'SecretoLlave' # esto es para el flash
URL_ORIGINAL = "https://api.openweathermap.org/data/2.5/weather?id="
API_KEY = open('api_key','r').read()

# Conectarse a la base de datos
mongo_uri = "mongodb://root:example@mongo:27017/mydatabase?authSource=admin" 
client = MongoClient(mongo_uri)
db = client.mydatabase


@app.route('/', methods=[ 'GET', 'POST'])
def index():
    
    error_msg = ''
    datosTiempo = None
    ciudad = None
    if request.method == 'POST':
        ciudad = request.form['ciudad']
        print(f"Ciudad recibida: {ciudad}")


        if not ciudad:
            error_msg = "Introduzca una ciudad"
            
        else:
            datosTiempo = get_datosTiempo(ciudad)
            if datosTiempo == 'Error':
                error_msg = 'Esa no es una ciudad válida!'
                # Crear un nuevo diccionario con solo los atributos que quieres insertar
            else:

                fecha_hora_actual = datetime.now()

                
                formato_deseado = " %d-%m-%Y %H:%M:%S" # transforma en este formato la fecha y hora actual
                fecha_hora_format = fecha_hora_actual.strftime(formato_deseado)

                datos = {
                    'lugar': datosTiempo.lugar,
                    'tempAct': datosTiempo.tempAct,
                    'tempMin': datosTiempo.tempMin,
                    'tempMax': datosTiempo.tempMax,
                    'humedad': datosTiempo.humedad,
                    'descrip': datosTiempo.descrip,
                    'icono': datosTiempo.icono,
                    'fecha': fecha_hora_format, # Añadir la fecha actual
                    'pais' : datosTiempo.pais
                }

                db.ciudades.insert_one(datos)
                print(datosTiempo)
                #db.ciudades.insert_one(datosTiempo.__dict__)

        if error_msg:
            flash(error_msg, 'error')
        else:
            flash('Ciudad añadida exitosamente!', 'success')

    return render_template('index.html', data=datosTiempo)

@app.route('/cities', methods=['GET', 'POST'])
def cities():
    if request.method == 'GET':
        lista = db.ciudades.find() # Devuelve una lista con todas las ciudades guardadas en bd

        return render_template('cities.html', data=lista)

    elif request.method == 'POST':
        
        ciudad_id = request.form.get('ciudad_id')
        
        db.ciudades.delete_one({'_id': ObjectId(ciudad_id)})
        return redirect('/cities')


@app.route('/registro', methods=['GET'])
def registro():
    if request.method == 'GET':
        if db.almacen_tiempo.count_documents({}) > 15:  # Si hay más de 15 registros, hace reset
            db.almacen_tiempo.delete_many({})
    
        lista = list(db.almacen_tiempo.find())  # Convertir el cursor a una lista antes de pasarlo al template
        return render_template('registro.html', data=lista)

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000, debug=True)
