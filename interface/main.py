from household_package.data import call_data_url
from household_package.data import call_data_cloud
from household_package.clean import clean_data
from household_package.model import baseline_model
from household_package.model import get_xy
from sklearn.model_selection import train_test_split
from household_package.registry import save_model
import pickle



df = call_data_url()
#df2 = call_data_cloud()
df2 = clean_data(df)
X , y = get_xy(df2)
X_train, X_test, y_train, y_test =  train_test_split(X,y, test_size=0.3)

model = baseline_model(X_train, y_train)
model_save = save_model(model)

# file_path = "/home/dicanadu/code/dicanadu/01-household-energy/model_h5/baseline/baseline_20231129-113413.pkl"

# with open(file_path, 'rb') as file:
#     loaded_model = pickle.load(file)
#     print(loaded_model)

# print(loaded_model.score(X_test, y_test))


#print(model.score(X_test, y_test))

#print(df2.head())
