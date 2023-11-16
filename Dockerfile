FROM python:3-alpine3.15

WORKDIR /entrega

COPY . /entrega/

RUN pip install -r requirements.txt

EXPOSE 3000

CMD python ./app.py
