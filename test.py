import requests

url = 'http://localhost:8000/predict'

params = {
    'state_name': 'TX'
}

response = requests.get(url, params=params)
result = response.json() #=> {wait: 64}

print(result["kwh_prediction"])
