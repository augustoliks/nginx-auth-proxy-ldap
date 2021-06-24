FROM python:3.7-slim-buster

ENV FLASK_ENV production
ENV LOG_LEVEL DEBUG

WORKDIR /app

COPY src .
ADD requirements.txt .

RUN apt-get update -y
RUN apt-get install -y libsasl2-dev python-dev libldap2-dev libssl-dev gcc

RUN pip3 install -r requirements.txt

CMD gunicorn --bind 0.0.0.0:5000 --log-level debug entrypoint:app
