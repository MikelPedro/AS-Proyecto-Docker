FROM python:3-alpine3.15

WORKDIR /entrega
COPY . /entrega
# Instala las dependencias

RUN pip install -r requirements.txt

# Copia los archivos de la aplicación Flask
COPY . /entrega
# Expone el puerto en el que Flask se ejecutará
EXPOSE 5000

# Comando para ejecutar la aplicación Flask
CMD ["python", "webtiempo.py"]
