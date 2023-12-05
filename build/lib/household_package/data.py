import pandas as pd
from google.cloud import bigquery


def call_data_url():
    """This function calls the dataset choosen to deploy the package"""

    columns = ["REGIONC", "state_name", "BA_climate", "TYPEHUQ", "STORIES", "YEARMADERANGE", "NCOMBATH", "NHAFBATH", "TOTROOMS", "WALLTYPE", "ROOFTYPE", "WINDOWS",
           "SWIMPOOL", "NUMFRIG", "MICRO", "DISHWASH", "CWASHER", "DRYER", "TVCOLOR", "DESKTOP", "NUMLAPTOP",
           "TELLWORK","HEATHOME", "EQUIPM", "NUMPORTEL", "AIRCOND", "LGTIN1TO4", "LGTIN4TO8", "LGTINMORE8", "SMARTMETER", "SOLAR", "NHSLDMEM", "SQFTEST",
          "KWH", "DOLLAREL"]

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

    columns = ["REGIONC", "state_name", "BA_climate", "TYPEHUQ", "STORIES", "YEARMADERANGE", "NCOMBATH", "NHAFBATH", "TOTROOMS", "WALLTYPE", "ROOFTYPE", "WINDOWS",
           "SWIMPOOL", "NUMFRIG", "MICRO", "DISHWASH", "CWASHER", "DRYER", "TVCOLOR", "DESKTOP", "NUMLAPTOP",
           "TELLWORK","HEATHOME", "EQUIPM", "NUMPORTEL", "AIRCOND", "LGTIN1TO4", "LGTIN4TO8", "LGTINMORE8", "SMARTMETER", "SOLAR", "NHSLDMEM", "SQFTEST",
          "KWH", "DOLLAREL"]

    client = bigquery.Client()
    query_job = client.query(query)
    result = query_job.result()
    df = result.to_dataframe()

    return df[columns]

def make_X_new(user_input):
    """
    This functions takes a dictionary coming from user inputs
    and makes a one row of X for model prediciton.
    """
    ## get all the passed arguments
    #user_inputs = locals().copy()
    X_new = pd.DataFrame({k:[v] for k,v in user_input.items()})
    return X_new

if __name__ == '__main__':
    df = call_data_url()
    print(df.head())
