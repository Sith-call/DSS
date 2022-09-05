FROM ubuntu:latest

WORKDIR /backend/
COPY dss /backend/
COPY requirements.txt /backend/

RUN apt-get update
RUN apt-get install -y python3 pip

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV Django_secret_key secret_value

EXPOSE 8000

CMD python3 manage.py runserver 0.0.0.0:8000
