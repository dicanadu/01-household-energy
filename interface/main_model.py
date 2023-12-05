from household_package.data import call_data_url
from household_package.data import call_data_cloud
from household_package.clean import clean_data_without
from household_package.model import baseline_model_without
from household_package.model import get_xy
from sklearn.model_selection import train_test_split
from household_package.registry import save_model
from household_package.preprocessor import preprocessing
from household_package.registry import load_model
from household_package.registry import load_model_locally_log
from household_package.clean import filter_data
from household_package.data import make_X_new
from sklearn.model_selection import cross_validate
from household_package.model import baseline_model_improved
from household_package.clean import clean_data_improved

import pickle
import pandas as pd
import numpy as np


#This is a model without two features and with the log
df = call_data_url()
df = filter_data(df)
df["PRICEKWH"] =  df["DOLLAREL"] /df["KWH"]
df = clean_data_improved(df)
print(df.columns)

#columns = ["WALLTYPE", "ROOFTYPE", "TELLWORK", "REGIONC", "SOLAR"]
#df = df.drop(columns , axis =1 )

X , y = get_xy(df)
#print(X.columns)

X_train , X_test, y_train, y_test = train_test_split(X , y , test_size=0.3)
print(X_train.columns)

y_train_p = np.log(y_train.astype("float"))
y_test_p = np.log(y_test.astype("float"))

#model = baseline_model_improved(X_train, y_train_p)

# print(model.score(X_test, y_test_p))
# print(cross_validate(model, X_train, y_train_p)["test_score"].mean())

#To be used when saving a new model
#save_model(model)

model_new = load_model()


print(cross_validate(model_new, X_train, y_train_p)["test_score"].mean())


# for x , y  in zip(model_new[:-1].get_feature_names_out() ,model_new.named_steps["model"].coef_):
#     print(x , y)
