from flask import Flask, render_template, request
from tiempo import main as get_datosTiempo
app = Flask(__name__, template_folder='./app')

URL_ORIGINAL = "https://api.openweathermap.org/data/2.5/weather?id="
API_KEY = open('api_key','r').read()


    

@app.route('/', methods=[ 'GET', 'POST'])
def index():
    print("2222")
    datosTiempo = None
    print("444")

    if request.method == 'POST':
        
        ciudad = request.form['ciudad']
        print(f"Ciudad recibida: {ciudad}")
        datosTiempo = get_datosTiempo(ciudad)
        print(datosTiempo)

    return render_template('index.html', data=datosTiempo, ciudad=ciudad) # solo renderiza este html

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=int("3000"),debug=True)