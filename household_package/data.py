import pandas as pd
from google.cloud import bigquery


def call_data_url():
    """This function calls the dataset choosen to deploy the package"""

    columns = ["REGIONC", "state_name", "BA_climate", "TYPEHUQ", "STORIES", "YEARMADERANGE", "NCOMBATH", "NHAFBATH", "TOTROOMS", "WALLTYPE", "ROOFTYPE", "WINDOWS",
           "SWIMPOOL", "NUMFRIG", "MICRO", "DISHWASH", "CWASHER", "DRYER", "TVCOLOR", "DESKTOP", "NUMLAPTOP",
           "TELLWORK","HEATHOME", "EQUIPM", "NUMPORTEL", "AIRCOND", "LGTIN1TO4", "LGTIN4TO8", "LGTINMORE8", "SMARTMETER", "SOLAR", "NHSLDMEM", "SQFTEST",
          "KWH"]

    df = pd.read_csv("https://www.eia.gov/consumption/residential/data/2020/csv/recs2020_public_v6.csv",
                     usecols=columns)
    return df


def call_data_cloud():
    PROJECT = "wagon-bootcamp-401514"
    DATASET = "01_household_energy"
    TABLE = "recs2020"

    query = f"""
        SELECT *
        FROM `{PROJECT}.{DATASET}.{TABLE}`
        """

    client = bigquery.Client()
    query_job = client.query(query)
    result = query_job.result()
    df = result.to_dataframe()

    return df

if __name__ == '__main__':
    df = call_data_url()
    print(df.head())
