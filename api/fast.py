from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware


from datetime import datetime
import pytz

import pandas as pd

import joblib



PATH_TO_LOCAL_MODEL = "model.joblib"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get("/")
def index():
    return {"greeting": "Hello world"}



@app.get("/predict")
def predict(pickup_datetime ,
            pickup_longitude,
            pickup_latitude,
            dropoff_longitude,
            dropoff_latitude,
            passenger_count):
    # create a datetime object from the user provided datetime
    pickup_datetime = datetime.strptime(pickup_datetime, "%Y-%m-%d %H:%M:%S")
    # localize the user datetime with NYC timezone
    eastern = pytz.timezone("US/Eastern")
    localized_pickup_datetime = eastern.localize(pickup_datetime, is_dst=None)
    utc_pickup_datetime = localized_pickup_datetime.astimezone(pytz.utc)
    formatted_pickup_datetime = utc_pickup_datetime.strftime(
        "%Y-%m-%d %H:%M:%S UTC")

    r = {"key": [formatted_pickup_datetime],
        'pickup_datetime': [formatted_pickup_datetime],
        'pickup_longitude': [float(pickup_longitude)],
        'pickup_latitude': [float(pickup_latitude)],
        'dropoff_longitude': [float(dropoff_longitude)],
        'dropoff_latitude': [float(dropoff_latitude)],
        'passenger_count': [int(passenger_count)]
    }

    X_pred_DataFrame = pd.DataFrame.from_dict(r)


    model = joblib.load(PATH_TO_LOCAL_MODEL)
    pred = float(model.predict(X_pred_DataFrame))
    return {"prediction": pred}
