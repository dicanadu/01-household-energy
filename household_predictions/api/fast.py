import pandas as pd
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
# from taxifare.ml_logic.preprocessor import preprocess_features
from household_package.registry import load_model
from household_package.clean import clean_data


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
async def predict(request: Request
    #TYPEHUQ: int,
    #STORIES: int,
    #YEARMADERANGE: int,
    #WALLTYPE: int,
    #ROOFTYPE: int,
    #WINDOWS: int,
    #SWIMPOOL: int,
    #DISHWASH: int,
    #CWASHER: int,
    #DRYER: int,
    #TELLWORK: int,
    #TELLDAYS: int,
    #HEATHOME: int,
    #EQUIPM: int,
    #NUMPORTEL: int,
    #AIRCOND: int,
    #NUMPORTAC: int,
    #SMARTMETER: int,
    #SOLAR: int,
    #NCOMBATH: int,
    #NHAFBATH: int,
    #TOTROOMS: int,
    #NUMFRIG: int,
    #MICRO: int,
    #TVCOLOR: int,
    #DESKTOP: int,
    #NUMLAPTOP: int,
    #LGTIN1TO4: int,
    #LGTIN4TO8: int,
    #LGTINMORE8: int,
    #NHSLDMEM: int,
    #SQFTEST: int
    ):
    """
     Make a prediction based on user inputs.
     Baseline model is the default and is pulled from the cloud.
     """

    ### get params
    params = dict(request.query_params)

    ##### Create new dataframe from user inputs ######
    X_new = pd.DataFrame({k:[int(v) if v.isdigit() else v] for k,v in params.items()})

    ## clean the dataframe
    X_new_clean = clean_data(X_new)

    y_pred = app.state.model.predict(X_new_clean)

    return {'kwh_prediction': int(y_pred)}


@app.get("/getUserInfo")
def getUserInfo(request:Request):
    params = dict(request.query_params)
    #params = locals().copy() #**params
    return params


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
