from household_package.data import call_data_url
from household_package.data import call_data_cloud
from household_package.clean import clean_data
from household_package.model import baseline_model
from household_package.model import get_xy
from sklearn.model_selection import train_test_split
from household_package.registry import save_model
from household_package.preprocessor import preprocessing
from household_package.registry import load_model
import pickle



#df = call_data_url()
df = call_data_url()
#print(df.head())
df2 = clean_data(df)
# print(df2.shape)
# #print(df2.head())
X , y = get_xy(df2)

X_train, X_test, y_train, y_test =  train_test_split(X,y, test_size=0.3)

# preprocesor = preprocessing(X_train)
# X_train_prep = preprocesor.transform(X_train)
# X_test_prep = preprocesor.transform(X_test)
# #print(X_test_prep.shape)

#model = baseline_model(X_train, y_train)
#print(model.score(X_test, y_test))
model_cloud = load_model()
#save_model(model)

# file_path = "/home/dicanadu/code/dicanadu/01-household-energy/model_h5/baseline/baseline_20231129-113413.pkl"

# with open(file_path, 'rb') as file:
#     loaded_model = pickle.load(file)
#     print(loaded_model)

# print(loaded_model.score(X_test, y_test))


#print(model.score(X_test, y_test))

#print(df2.head())
