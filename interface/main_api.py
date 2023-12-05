import requests

user_input = {
  "TYPEHUQ": 4,
  "NHSLDMEM": 2,
  "state_name": "Arizona",
  #"REGIONC": "SOUTH",
  "BA_climate": "Hot-Humid",
  "SQFTEST": 500,
  "STORIES": 1,
  "YEARMADERANGE": 1,
  "NCOMBATH": 0,
  "NHAFBATH": 0,
  "TOTROOMS": 5,
  "WINDOWS": 1,
  "SWIMPOOL": 1,
  #"SOLAR": 1,
  "SMARTMETER": 1,
  #"TELLWORK": 1,
  "DESKTOP": 0,
  "NUMLAPTOP": 0,
  "TVCOLOR": 0,
  "DISHWASH": 1,
  "MICRO": 0,
  "NUMFRIG": 1,
  "CWASHER": 1,
  "DRYER": 1,
  "LGTIN1TO4": 0,
  "LGTIN4TO8": 0,
  "LGTINMORE8": 0,
  "AIRCOND": 1,
  "EQUIPM": 3,
  "HEATHOME": 1,
  "NUMPORTEL": 0,
  "PRICEKWH" : 0.13
  }

#url = "https://household-predictions-apilog-jaiabuy6eq-ew.a.run.app/predict"
#url2 = "https://household-predictions-apilog-improved-jaiabuy6eq-ew.a.run.app/predict"
# url3= "http://localhost:8000/predict"
url = "https://household-predictions-final-jaiabuy6eq-ew.a.run.app/predict"
#65print("Im a running")


response = requests.get(url, user_input)
#print(response.content)
print(response.json())
