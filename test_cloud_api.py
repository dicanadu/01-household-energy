import requests

url = "https://householdpredictions-jaiabuy6eq-ew.a.run.app/predict"

# url = "https://dicanadu-er4hx24myq-ew.a.run.app/predict"

state_name = 'TX'

params = {
    'state_name': state_name, # 0 for Sunday, 1 for Monday, ...

}
response = requests.get(url,params=params)

# print(response.status_code)

print(response.json()["kwh_prediction"])

# &&pickup_longitude=-73.950655&pickup_latitude=40.783282&dropoff_longitude=-73.984365&dropoff_latitude=40.769802&passenger_count=2


# 40.70617433500528, -74.0088148740345
