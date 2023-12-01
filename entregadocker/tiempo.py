import requests
from dataclasses import dataclass

URL_ORIGINAL = "https://api.openweathermap.org/data/2.5/weather?q="
API_KEY = open('api_key','r').read()

@dataclass
class Tiempo:
    lugar: str
    tempAct: float
    tempMin: float
    tempMax: float
    humedad: int
    descrip: str
    icono: str
    code: int
    pais: str

def get_datosTiempo(ciudad,API_KEY):
    respuesta = requests.get(URL_ORIGINAL + str(ciudad) + "&appid=" + str(API_KEY)+ "&units=metric")

    datos = respuesta.json()
    print(datos)
    if datos['cod'] == 200:
        data = Tiempo(
            lugar = ciudad,
            tempAct = datos['main']['temp'],
            tempMin = datos['main']['temp_min'],
            tempMax = datos['main']['temp_max'],
            humedad = datos['main']['humidity'],
            descrip = datos['weather'][0]['description'],
            icono = datos['weather'][0]['icon'],
            code = datos['cod'],
            pais = datos['sys']['country']
        )
    else:
        data = 'Error'
    return data

def main(ciudad):

    datosTiempo = get_datosTiempo(ciudad,API_KEY)
    print(datosTiempo)
    return datosTiempo