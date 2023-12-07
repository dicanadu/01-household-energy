import requests

user_input = {
  "TYPEHUQ": 2,
  "SQFTEST": 1530,
  "NHSLDMEM": 2,
  "state_name": "California",
  "PRICEKWH": 0.2999,
  "BA_climate": "Cold",
  "TOTROOMS": 6,
  "STORIES": 1,
  "YEARMADERANGE": 4,
  "HEATHOME": 1,
  "SMARTMETER": 0,
  "NCOMBATH": 2,
  "NHAFBATH": 0,
  "EQUIPM": 3,
  "WINDOWS": 4,
  "SWIMPOOL": 0,
  "DESKTOP": 0,
  "NUMLAPTOP": 0,
  "MICRO": 1,
  "NUMPORTEL": 0,
  "CWASHER": 1,
  "AIRCOND": 1,
  "TVCOLOR": 2,
  "NUMFRIG": 1,
  "LGTIN1TO4": 4,
  "LGTIN4TO8": 0,
  "LGTINMORE8": 0,
  "DRYER": 1,
  "DISHWASH": 1
}

#url = "https://household-predictions-apilog-jaiabuy6eq-ew.a.run.app/predict"
#url2 = "https://household-predictions-apilog-improved-jaiabuy6eq-ew.a.run.app/predict"
url3= "https://us-electricity-estimator-jaiabuy6eq-ew.a.run.app/predict"
#url = "https://household-predictions-final-jaiabuy6eq-ew.a.run.app/predict"

url2 = "https://household-predictions-final2-jaiabuy6eq-ew.a.run.app/predict"
#65print("Im a running")

print("TEsting FINAL")
response = requests.get(url3, user_input)
#print(response.content)
print(response.json())

print("TEsting FINAL 2")
response = requests.get(url2, user_input)
#print(response.content)
print(response.json())
