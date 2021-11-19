FROM python:3.8.12-buster

COPY api /api
COPY requirements.txt /requirements.txt
COPY model.joblib /model.joblib
COPY TaxiFareModel /TaxiFareModel
COPY /home/johana/code/jomerabe/gcp/wagon-bootcamp-328014-127e896b378f.json /credentials.json


RUN pip install --upgrade pip &&\
pip install -r requirements.txt

CMD uvicorn api.fast:app --host 0.0.0.0 --port $PORT
