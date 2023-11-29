import pandas as pd

def call_data():
    """This function calls the dataset choosen to deploy the package"""

    columns = ["REGIONC", "state_name", "BA_climate", "TYPEHUQ", "STORIES", "YEARMADERANGE", "NCOMBATH", "NHAFBATH", "TOTROOMS", "WALLTYPE", "ROOFTYPE", "WINDOWS",
           "SWIMPOOL", "NUMFRIG", "MICRO", "DISHWASH", "CWASHER", "DRYER", "TVCOLOR", "DESKTOP", "NUMLAPTOP",
           "TELLWORK", "TELLDAYS","HEATHOME", "EQUIPM", "NUMPORTEL", "AIRCOND", "LGTIN1TO4", "LGTIN4TO8", "LGTINMORE8", "SMARTMETER", "SOLAR", "NHSLDMEM", "SQFTEST",
          "KWH"]
    df = pd.read_csv("https://www.eia.gov/consumption/residential/data/2020/csv/recs2020_public_v6.csv",
                     usecols=columns)
    return df

if __name__ == '__main__':
    df = call_data()
    print(df.head())
