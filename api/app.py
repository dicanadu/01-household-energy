import pandas as pd

#from household_package.registry import load_model
#from household_package.preprocessor import preprocess_features

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from household_package.clean import clean_data
from household_package.registry import load_model
from household_package.registry import load_model_locally

app = FastAPI()
app.state.model = load_model_locally()

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
    # $CHA_BEGIN
    return dict(greeting="Hello")
    # $CHA_END

@app.get("/predict")
def predict(
    TYPEHUQ: int,
    NHSLDMEM: int,
    state_name: str,
    REGIONC: str,
    BA_climate: str,
    SQFTEST: int,
    STORIES: int,
    YEARMADERANGE: int,
    NCOMBATH: int,
    NHAFBATH: int,
    TOTROOMS: int,
    WALLTYPE: int,
    ROOFTYPE: int,
    WINDOWS: int,
    SWIMPOOL: int,
    SOLAR: int,
    SMARTMETER: int,
    TELLWORK: int,
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
    NUMPORTEL: int
    ):
    """
     Make a prediction based on user inputs.
     Baseline model is the default and is pulled from the cloud.
     """

    ### get params
    #params = dict(request.query_params)
    params = locals()
    X_new = pd.DataFrame(params, index=[0])
    X_new = clean_data(X_new)
    ##### Create new dataframe from user inputs ######
    #X_new = pd.DataFrame({k:[int(v) if v.isdigit() else v] for k,v in params.items()})

    # # ## clean the dataframe
    y_pred = app.state.model.predict(X_new)[0]

    return {"KWH": y_pred}
    #return params
