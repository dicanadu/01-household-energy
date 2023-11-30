from household_package.data import call_data_url
from household_package.data import call_data_cloud
from household_package.clean import clean_data
from household_package.model import baseline_model
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

user_input = {
  "TYPEHUQ": 1,
  "NHSLDMEM": 1,
  "state_name": "Alabama",
  "REGIONC": "SOUTH",
  "BA_climate": "Hot-Humid",
  "SQFTEST": 240,
  "STORIES": 1,
  "YEARMADERANGE": 1,
  "NCOMBATH": 0,
  "NHAFBATH": 0,
  "TOTROOMS": 1,
  "WALLTYPE": 1,
  "ROOFTYPE": 1,
  "WINDOWS": 1,
  "SWIMPOOL": 1,
  "SOLAR": 1,
  "SMARTMETER": 1,
  "TELLWORK": 1,
  "DESKTOP": 0,
  "NUMLAPTOP": 0,
  "TVCOLOR": 0,
  "DISHWASH": 1,
  "MICRO": 0,
  "NUMFRIG": 0,
  "CWASHER": 1,
  "DRYER": 1,
  "LGTIN1TO4": 0,
  "LGTIN4TO8": 0,
  "LGTINMORE8": 0,
  "AIRCOND": 1,
  "EQUIPM": 3,
  "HEATHOME": 1,
  "NUMPORTEL": 0
}

#X_new = clean_data(make_X_new(user_input))
#print(X_new)
df = call_data_url()
#df = call_data_url()
#print(df.head())
df = filter_data(df)
print(df["YEARMADERANGE"].unique())
# #print(df2.head())
X , y = get_xy(df)
df = clean_data(X)
#print(X.loc[0,:])

#print(X.shape)

X_train, X_test, y_train, y_test =  train_test_split(X,y, test_size=0.3)
y_train_prep = np.log(y_train)
y_test_prep = np.log(y_test)

#X_row = pd.DataFrame(X_train.loc[0,:]).T
#print(X_row.columns)
#print(X_train)


# preprocesor = preprocessing(X_train)
# # X_train_prep = preprocesor.transform(X_train)
# # X_test_prep = preprocesor.transform(X_test)

model_1 = baseline_model(X_train, y_train)
#print(model_1.score(X_test, y_test))
scores = cross_validate(model_1, X_train, y_train, cv=5)
print(scores["test_score"].mean())
#model_cloud = load_model()
model_2 = baseline_model(X_train, y_train_prep)
scores = cross_validate(model_2, X_train, y_train_prep, cv=5)
print(scores["test_score"].mean())
#print(model_2.score(X_test, y_test_prep))
#print(model_cloud.predict(X_new))
#print(model_cloud.predict(X_row))
#save_model(model)

# file_path = "/home/dicanadu/code/dicanadu/01-household-energy/model_h5/baseline/baseline_20231129-113413.pkl"

# with open(file_path, 'rb') as file:
#     loaded_model = pickle.load(file)
#     print(loaded_model)

# print(loaded_model.score(X_test, y_test))


#print(model.score(X_test, y_test))

#print(df2.head())
