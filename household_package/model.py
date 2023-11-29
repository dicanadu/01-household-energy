from sklearn.linear_model import LinearRegression

def get_xy(df):
    X = df.drop("KWH",axis=1)
    y = df["KWH"]
    return X , y

def baseline_model(X_train, y_train):
    model = LinearRegression().fit(X_train, y_train)
    return model

#here parameters should be set features of the model
# def prediction(X_new: np.ndarray):
#     y_pred = model.predict(X_new)
#     return y_pred
