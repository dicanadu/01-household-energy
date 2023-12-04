from household_package.data import call_data_url
from household_package.data import call_data_cloud
from household_package.clean import clean_data_without
from household_package.model import baseline_model_without
from household_package.model import get_xy
from sklearn.model_selection import train_test_split
from household_package.registry import save_model
from household_package.preprocessor import preprocessing
from household_package.registry import load_model
from household_package.clean import filter_data
from household_package.data import make_X_new
from sklearn.model_selection import cross_validate

import pickle
import pandas as pd
import numpy as np


#This is a model without two features and with the log
df = call_data_url()
df = filter_data(df)
df = clean_data_without(df)

columns = ["WALLTYPE", "ROOFTYPE"]
df = df.drop(columns , axis =1 )

X , y = get_xy(df)

X_train , X_test, y_train, y_test = train_test_split(X , y , test_size=0.3)

y_train_p = np.log(y_train.astype("float"))
y_test_p = np.log(y_test.astype("float"))

model = baseline_model_without(X_train, y_train_p)

print(model.score(X_test, y_test_p))

#To be used when saving a new model
#save_model(model)

model_new = load_model()
