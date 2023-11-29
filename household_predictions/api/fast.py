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
    # Step 1:
        # Preproc & transform

    # Step 2:
        # Load Model

    # Step 3:
        # model.predict

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
