import pandas as pd
import numpy as np

#from household_package.registry import load_model
#from household_package.preprocessor import preprocess_features

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from household_package.clean import clean_data
from household_package.clean import clean_data_without
from household_package.clean import clean_data_improved
from household_package.registry import load_model
from household_package.registry import load_model_locally
from household_package.registry import load_model_locally_log

app = FastAPI()
app.state.model = load_model_locally_log()

# Allowing all middleware is optional, but good practice for dev purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def root():
    root_dict = {
    "api_version": "1.0",
    "endpoints": {
        "predict": {
        "url": "/predict",
        "description": "Endpoint for retrieving kwh predictions",
        "methods": ["GET"]
            }
        }
    }
    return root_dict

# #Predict baseline
# @app.get("/predict")
# def predict(
#     TYPEHUQ: int,
#     NHSLDMEM: int,
#     state_name: str,
#     REGIONC: str,
#     BA_climate: str,
#     SQFTEST: int,
#     STORIES: int,
#     YEARMADERANGE: int,
#     NCOMBATH: int,
#     NHAFBATH: int,
#     TOTROOMS: int,
#     WALLTYPE: int,
#     ROOFTYPE: int,
#     WINDOWS: int,
#     SWIMPOOL: int,
#     SOLAR: int,
#     SMARTMETER: int,
#     TELLWORK: int,
#     DESKTOP: int,
#     NUMLAPTOP: int,
#     TVCOLOR: int,
#     DISHWASH: int,
#     MICRO: int,
#     NUMFRIG: int,
#     CWASHER: int,
#     DRYER: int,
#     LGTIN1TO4: int,
#     LGTIN4TO8: int,
#     LGTINMORE8: int,
#     AIRCOND: int,
#     EQUIPM: int,
#     HEATHOME: int,
#     NUMPORTEL: int
#     ):
#     """
#      Make a prediction based on user inputs.
#      Baseline model is the default and is pulled from the cloud.
#      """

#     ### get params
#     #params = dict(request.query_params)
#     params = locals()
#     X_new = pd.DataFrame(params, index=[0])
#     X_new = clean_data(X_new)
#     ##### Create new dataframe from user inputs ######
#     #X_new = pd.DataFrame({k:[int(v) if v.isdigit() else v] for k,v in params.items()})

#     # # ## clean the dataframe
#     y_pred = app.state.model.predict(X_new)[0]

#     return {"KWH": y_pred}
#     #return params

#Predict log baseline
@app.get("/predict")
def predict(
    TYPEHUQ: int,
    NHSLDMEM: int,
    state_name: str,
    #REGIONC: str,
    BA_climate: str,
    SQFTEST: int,
    STORIES: int,
    YEARMADERANGE: int,
    NCOMBATH: int,
    NHAFBATH: int,
    TOTROOMS: int,
    WINDOWS: int,
    SWIMPOOL: int,
    #SOLAR: int,
    SMARTMETER: int,
    #TELLWORK: int,
    DESKTOP: int,
    NUMLAPTOP: int,
    TVCOLOR: int,
    DISHWASH: int,
    MICRO: int,
    NUMFRIG: int,
    CWASHER: int,
    DRYER: int,
    LGTIN1TO4: int,
    LGTIN4TO8: int,
    LGTINMORE8: int,
    AIRCOND: int,
    EQUIPM: int,
    HEATHOME: int,
    NUMPORTEL: int,
    PRICEKWH: float
    ):
    """
     Make a prediction based on user inputs.
     Baseline model is the default and is pulled from the cloud.
     """

    ### get params
    #params = dict(request.query_params)
    params = locals()
    X_new = pd.DataFrame(params, index=[0])
    X_new = clean_data_improved(X_new)
    ##### Create new dataframe from user inputs ######
    #X_new = pd.DataFrame({k:[int(v) if v.isdigit() else v] for k,v in params.items()})

    # # ## clean the dataframe
    y_pred = app.state.model.predict(X_new)[0]
    y_pred = np.exp(y_pred)
    #print("Im a running")

    return {"KWH": y_pred}
    #return params
