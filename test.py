import requests

url = 'http://localhost:8000/predict'

params = {
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


response = requests.get(url, params=params)
result = response.json() #=> {wait: 64}

print(result["kwh_prediction"])
