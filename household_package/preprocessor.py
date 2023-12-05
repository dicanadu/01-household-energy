from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler

def preprocessing(X_train):
    to_ohe_encode = ['REGIONC', 'state_name','BA_climate','TYPEHUQ',
                     'YEARMADERANGE','WALLTYPE','ROOFTYPE','WINDOWS','EQUIPM']
    to_scale = ["NUMPORTEL", "STORIES","SQFTEST",
            "TOTROOMS", "NUMFRIG", "MICRO", "TVCOLOR","NHSLDMEM",
            "TOTAL_BATH", "TOTAL_COMP", "TOTAL_LIGHT" ]
    to_standard = ["KWH"]

    min_max = MinMaxScaler()
    ohe = OneHotEncoder(sparse_output=False, handle_unknown='ignore',drop="first")
    std = StandardScaler()


    preprocessor = ColumnTransformer(transformers=[
                                                ('min_max', min_max, to_scale),
                                                ('ohe', ohe, to_ohe_encode),
                                                ('std'), std,to_standard ],
                                                    remainder = "passthrough")

    return preprocessor.fit(X_train)
