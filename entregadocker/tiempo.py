import requests
from dataclasses import dataclass

URL_ORIGINAL = "https://api.openweathermap.org/data/2.5/weather?q="
API_KEY = open('api_key','r').read()
URL_POLUCION = "http://api.openweathermap.org/data/2.5/air_pollution?"


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
    calidad: str



def get_datosTiempo(ciudad,API_KEY):
    respuesta = requests.get(URL_ORIGINAL + str(ciudad) + "&appid=" + str(API_KEY)+ "&units=metric")

    datos = respuesta.json()
    
    if datos['cod'] == 200:

        lon = datos['coord']['lon']
        lat = datos['coord']['lat']

        respuesta_pol = requests.get(URL_POLUCION + "lat=" + str(lat) + "&lon=" + str(lon) + "&appid=" + str(API_KEY))

        datospol = respuesta_pol.json()

        if datospol['list'][0]['main']['aqi'] == 1:
            aire = 'Buena'
        elif datospol['list'][0]['main']['aqi'] == 2:
            aire = 'Moderada'    
        elif datospol['list'][0]['main']['aqi'] == 3:   
            aire = 'Poco saludable'  
        elif datospol['list'][0]['main']['aqi'] == 4:   
            aire = 'Insalubre'   
        elif datospol['list'][0]['main']['aqi'] == 5:   
            aire = 'Muy insalubre'   

        data = Tiempo(
            lugar = ciudad,
            tempAct = datos['main']['temp'],
            tempMin = datos['main']['temp_min'],
            tempMax = datos['main']['temp_max'],
            humedad = datos['main']['humidity'],
            descrip = datos['weather'][0]['description'],
            icono = datos['weather'][0]['icon'],
            code = datos['cod'],
            pais = datos['sys']['country'],
            calidad = aire
        )
    else:
        data = 'Error'
    
    return data


def main(ciudad):

    datosTiempo = get_datosTiempo(ciudad,API_KEY)
    print(datosTiempo)
    return datosTiempo
