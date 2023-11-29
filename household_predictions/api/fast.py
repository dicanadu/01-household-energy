import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from taxifare.ml_logic.preprocessor import preprocess_features
from household_package.registry import load_model
from household_package.data import clean_data, preprocessing, call_data_url
import random

app = FastAPI()
app.state.model = load_model()

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
    SQFTEST: int):
    """
     Make a prediction based on user inputs.
     Baseline model is the default and is pulled from the cloud.
     """
    ##### Create new dataframe from user inputs ######

    ## get all the passed arguments
    user_inputs = locals().copy()

    ## make a dataframe
    ## values of the dict should be lists
    X_new = pd.DataFrame({k:[v] for k,v in user_inputs.items()})

    ## clean the dataframe
    X_new_clean = clean_data(X_new)

    ## preprocessing - but we nee dX_train to fit it!
    ## otherwise it should be part of the pipeline stored in the cloud!
    X_train = clean_data(call_data_url()).drop(columns = 'KWH')
    preprocessor = preprocessing(X_train)
    X_new_processed = preprocessor.transform(X_new_clean)
    y_pred = app.state.model.predict(X_new_processed)

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
