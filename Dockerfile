FROM python:3-alpine3.15

WORKDIR /entrega

COPY . /entrega/

RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "webtiempo:app", "-b", "0.0.0.0:5000"]