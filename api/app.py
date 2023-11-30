import pandas as pd

#from household_package.registry import load_model
#from household_package.preprocessor import preprocess_features

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

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
async def predict(
    TYPEHUQ: int
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
