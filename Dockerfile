FROM python:3.9.18-bookworm

#RUN apt-get update && apt-get install -y python3 python3-pip
WORKDIR /opt

#RUN pip install flask
#RUN pip install requests
#RUN pip install oracledb
#RUN pip install datetime

COPY requirements.txt .
RUN pip install requirements.txt

COPY app.py /opt/

ENTRYPOINT FLASK_APP=/opt/app.py flask run --host=0.0.0.0 --port=8080
