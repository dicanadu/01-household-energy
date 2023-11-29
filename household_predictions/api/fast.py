import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from taxifare.ml_logic.preprocessor import preprocess_features
# from taxifare.ml_logic.registry import load_model
import random

app = FastAPI()
# app.state.model = load_model()

# Allowing all middleware is optional, but good practice for dev purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# http://127.0.0.1:8000/predict?pickup_datetime=2012-10-06 12:10:20&pickup_longitude=40.7614327&pickup_latitude=-73.9798156&dropoff_longitude=40.6513111&dropoff_latitude=-73.8803331&passenger_count=2
@app.get("/predict")
def predict(
    TYPEHUQ: int,
    STORIES: int,
    YEARMADERANGE: int,
    WALLTYPE: int,
    ROOFTYPE: int,
    WINDOWS: int,
    SWIMPOOL: int,
    DISHWASH: int,
    CWASHER: int,
    DRYER: int,
    TELLWORK: int,
    TELLDAYS: int,
    HEATHOME: int,
    EQUIPM: int,
    NUMPORTEL: int,
    AIRCOND: int,
    NUMPORTAC: int,
    SMARTMETER: int,
    SOLAR: int,
    NCOMBATH: int,
    NHAFBATH: int,
    TOTROOMS: int,
    NUMFRIG: int,
    MICRO: int,
    TVCOLOR: int,
    DESKTOP: int,
    NUMLAPTOP: int,
    LGTIN1TO4: int,
    LGTIN4TO8: int,
    LGTINMORE8: int,
    NHSLDMEM: int,
    SQFTEST: int
):
    #     pickup_datetime: str,  # 2013-07-06 17:18:00
    #     pickup_longitude: float,    # -73.950655
    #     pickup_latitude: float,     # 40.783282
    #     dropoff_longitude: float,   # -73.984365
    #     dropoff_latitude: float,    # 40.769802
    #     passenger_count: int
    # ):      # 1
    # """
    # Make a single course prediction.
    # Assumes `pickup_datetime` is provided as a string by the user in "%Y-%m-%d %H:%M:%S" format
    # Assumes `pickup_datetime` implicitly refers to the "US/Eastern" timezone (as any user in New York City would naturally write)
    # """
    # # X_pred = pd.DataFrame(locals())
    # X = {'pickup_datetime': pd.Timestamp(pickup_datetime, tz="US/Eastern"),
    #                   'pickup_longitude': pickup_longitude,
    #                   'pickup_latitude': pickup_latitude,
    #                   'dropoff_longitude': dropoff_longitude,
    #                   'dropoff_latitude': dropoff_latitude,
    #                   'passenger_count': passenger_count}

    # X_pred = pd.DataFrame([X])
    # X_processed = preprocess_features(X_pred)
    # y_pred = app.state.model.predict(X_processed)

    # return {'fare_amount': float(y_pred[0])}
    y_pred = random.randint(1000, 5000)

    return {'kwh_prediction': int(y_pred)}


@app.get("/")
def root():
    root_dict = {
    "api_version": "1.0",
    "base_url": "https://householdpredictions-jaiabuy6eq-ew.a.run.app",
    "endpoints": {
        "predict": {
        "url": "/predict",
        "description": "Endpoint for retrieving kwh predictions",
        "methods": ["GET"]
            }
        }
    }
    return root_dict