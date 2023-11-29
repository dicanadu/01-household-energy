import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

def clean_data(df):
    """This set cleans the data to have it in the correct format before preprocessing"""
    df = df.copy()
    #Maping features
    TYPEHUQ_map = {1: "Mobile", 2: "Single_detached",3: "Single_attached",
                   4: "Appartment_small" ,5: "Appartment_big"}
    YEARMADERANGE_map = {1: "Before_50", 2:"50-59", 3:"60-69",
                         4: "70-79", 5: "80-89", 6:"90-99", 7:"00-09",
                         8:"2010-15", 9:"2016-20" }
    WALLTYPE_map = {1:"Brick",2:"Wood",3:"Siding",4:"Stucco",5:"Shingle",
                    6:"Stone",7:"Concrete",99:"Other"}
    ROOFTYPE_map = {1 : "Ceramic", 2 : "Wood", 3 : "Metal", 4: "Slate",
                    5: "Shingle", 6: "Concrete", 99: "Other", -2:"Other"}
    EQUIPM_map = {3:"Furnace", 2: "Steam", 4: "Central_heat", 13: "Ductless_heat",
                5: "Electric_units", 7: "Room_heater", 8 : "Wood",
                10:"Electric_heater", 99:"Other", -2:"Other"}

    dics_transform = [TYPEHUQ_map, YEARMADERANGE_map, WALLTYPE_map, ROOFTYPE_map, EQUIPM_map]
    columns_to_transform = ["TYPEHUQ", "YEARMADERANGE", "WALLTYPE", "ROOFTYPE", "EQUIPM"]

    for x , y in zip(dics_transform,columns_to_transform):
        df[y] = df[y].map(x)

    #Combine new features
    df["TOTAL_BATH"] = df["NCOMBATH"] + df["NHAFBATH"]
    df.drop( ["NCOMBATH", "NHAFBATH"] ,axis=1, inplace = True)

    df["TOTAL_COMP"] = df["DESKTOP"] + df["NUMLAPTOP"]
    df.drop( ["DESKTOP", "NUMLAPTOP"] ,axis=1, inplace = True)

    df["TOTAL_LIGHT"] = df["LGTIN1TO4"] + df["LGTIN4TO8"] + df["LGTINMORE8"]
    df.drop( ["LGTIN1TO4", "LGTIN4TO8", "LGTINMORE8"] ,axis=1, inplace = True)

    df["STORIES"] = df["STORIES"].replace(-2,1)
    df["STORIES"] = df["STORIES"].replace(5,2)

    #Impute features
    features_imputer2 = ['SWIMPOOL', 'NUMPORTEL', 'SOLAR']
    features_imputer4 = ['SMARTMETER']
    #to_ohe_encode = ['REGIONC', 'state_name','BA_climate','TYPEHUQ','YEARMADERANGE','WALLTYPE','ROOFTYPE','WINDOWS','EQUIPM']

    imputer_2 = SimpleImputer(strategy='constant', missing_values=-2, fill_value=0)
    imputer_4 = SimpleImputer(strategy='constant', missing_values=-4, fill_value=0)
    #ohe = OneHotEncoder(sparse_output=False, handle_unknown='ignore')

    preprocessor = ColumnTransformer(transformers=[('imputer_2',imputer_2, features_imputer2),
                                                ('imputer_4',imputer_4, features_imputer4)],
                                                #('ohe', ohe, to_ohe_encode)],
                                                    remainder = "passthrough")

    preprocessor.fit(df)

    cols = [x.split("__")[1] for x in preprocessor.get_feature_names_out()]

    df_clean = pd.DataFrame(preprocessor.transform(df),
                       columns = cols)

    return df_clean
