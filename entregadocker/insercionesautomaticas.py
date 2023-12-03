from pymongo import MongoClient
from tiempo import main as get_datosTiempo
import random
import time
import os


URL_ORIGINAL = "https://api.openweathermap.org/data/2.5/weather?id="
API_KEY = open('api_key','r').read()
# Establece la conexión con el servidor MongoDB
mongo_uri = "mongodb://root:example@mongo:27017/mydatabase?authSource=admin" 


# Conectarse a la base de datos
client = MongoClient(mongo_uri)
db = client.mydatabase
coleccion = db.almacen_tiempo
# Leer ciudades desde el archivo
with open("list.txt", "r") as archivo:
    ciudades = archivo.read().splitlines()

# Función para realizar inserciones cada 30 segundos
def insertar_ciudad():
    ciudad = random.choice(ciudades)
    datosTiempo = get_datosTiempo(ciudad)
    datos = {
                'lugar': datosTiempo.lugar,
                'tempAct': datosTiempo.tempAct,
                'pais' : datosTiempo.pais,
                'calidad' : datosTiempo.calidad
            }

    coleccion.insert_one(datos)

# Ejecutar inserciones cada 30 segundos
while True:
    insertar_ciudad()
    time.sleep(30)

