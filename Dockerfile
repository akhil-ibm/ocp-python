FROM python:3.9.18-bookworm

#RUN apt-get update && apt-get install -y python3 python3-pip

RUN pip install flask, requests, oracledb, datetime

COPY login.py /opt/

ENTRYPOINT FLASK_APP=/opt/login.py flask run --host=0.0.0.0 --port=8081
