from sklearn.linear_model import LinearRegression
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import RobustScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline

def get_xy(df):
    X = df.drop("KWH",axis=1)
    y = df["KWH"]
    return X , y

def baseline_model(X_train, y_train):

    to_ohe_encode = ['REGIONC', 'state_name','BA_climate','TYPEHUQ',
                     'YEARMADERANGE','WALLTYPE','ROOFTYPE','WINDOWS','EQUIPM']
    to_scale = ["NUMPORTEL", "STORIES","SQFTEST",
                "TOTROOMS", "NUMFRIG", "MICRO", "TVCOLOR","NHSLDMEM",
                "TOTAL_BATH", "TOTAL_COMP", "TOTAL_LIGHT" ]

    min_max = MinMaxScaler()
    ohe = OneHotEncoder(sparse_output=False, handle_unknown='ignore')


    preprocessor = ColumnTransformer(transformers=[
                                                ('min_max', min_max, to_scale),
                                                ('ohe', ohe, to_ohe_encode)],
                                                remainder = "passthrough")

    model = LinearRegression()

    pipe = Pipeline([('prep', preprocessor), ('model', model)])

    return pipe.fit(X_train, y_train)

#here parameters should be set features of the model
# def prediction(X_new: np.ndarray):
#     y_pred = model.predict(X_new)
#     return y_pred

def baseline_model_without(X_train, y_train):

    to_ohe_encode = ['REGIONC', 'state_name','BA_climate','TYPEHUQ',
                     'YEARMADERANGE','WINDOWS','EQUIPM']
    to_scale = ["NUMPORTEL", "STORIES","SQFTEST",
                "TOTROOMS", "NUMFRIG", "MICRO", "TVCOLOR","NHSLDMEM",
                "TOTAL_BATH", "TOTAL_COMP", "TOTAL_LIGHT" ]

    min_max = MinMaxScaler()
    ohe = OneHotEncoder(sparse_output=False, handle_unknown='ignore')


    preprocessor = ColumnTransformer(transformers=[
                                                ('min_max', min_max, to_scale),
                                                ('ohe', ohe, to_ohe_encode)],
                                                remainder = "passthrough")

    model = LinearRegression()

    pipe = Pipeline([('prep', preprocessor), ('model', model)])

    return pipe.fit(X_train, y_train)

def baseline_model_improved(X_train, y_train):

    to_ohe_encode = ['state_name','BA_climate','TYPEHUQ',
                     'YEARMADERANGE','WINDOWS','EQUIPM']

    to_scale = ["NUMPORTEL", "STORIES","SQFTEST",
                "TOTROOMS", "NUMFRIG", "MICRO", "TVCOLOR","NHSLDMEM",
                "TOTAL_BATH", "TOTAL_COMP", "TOTAL_LIGHT" ]

    min_max = MinMaxScaler()
    ohe = OneHotEncoder(sparse_output=False, handle_unknown='ignore', drop="first")


    preprocessor = ColumnTransformer(transformers=[
                                                ('min_max', min_max, to_scale),
                                                ('ohe', ohe, to_ohe_encode)],
                                                remainder = "passthrough")

    model = LinearRegression()

    pipe = Pipeline([('prep', preprocessor), ('model', model)])

    return pipe.fit(X_train, y_train)
