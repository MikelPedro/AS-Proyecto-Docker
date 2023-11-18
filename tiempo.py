import requests
import os
from dataclasses import dataclass

URL_ORIGINAL = "https://api.openweathermap.org/data/2.5/weather?q="
API_KEY = open('api_key','r').read()

@dataclass
class Tiempo:
    tempAct: float
    tempMin: float
    tempMax: float
    humedad: int
    descrip: str
    icono: str

def get_datosTiempo(ciudad,API_KEY):
    respuesta = requests.get(URL_ORIGINAL + str(ciudad) + "&appid=" + str(API_KEY)+ "&units=metric")

    datos = respuesta.json()


    data = Tiempo(
        tempAct = datos['main']['temp'],
        tempMin = datos['main']['temp_min'],
        tempMax = datos['main']['temp_max'],
        humedad = datos['main']['humidity'],
        descrip = datos['weather'][0]['description'],
        icono = datos['weather'][0]['icon']
    )
    """
    print("Temp:" + str(tempAct) + "°C")
    print("TempMin:" + str(tempMin) + "°C")
    print("TempMax:" + str(tempMax) + "°C")
    print("Humedad:" + str(humedad))
    print("Descripcion:" + str(descrip))
    print("Icono:" + str(icono))

    """
    return data

def main(ciudad):

    datosTiempo = get_datosTiempo(ciudad,API_KEY)
    return datosTiempo