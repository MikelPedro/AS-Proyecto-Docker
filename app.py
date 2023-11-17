from flask import Flask, render_template 
app = Flask(__name__, template_folder='./app')

URL_ORIGINAL = "https://api.openweathermap.org/data/2.5/weather?id="
API_KEY = open('api_key','r').read()



def temperaturaACelsius():

    

@app.route('/', methods=['GET', 'POST'])
def index():
    # Puedes pasar datos a la plantilla, por ejemplo, un título
    title = 'Ejemplo de Flask y HTML'
    return render_template('index.html', title=title)

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=int("3000"),debug=True)