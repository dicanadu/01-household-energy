from household_package.data import call_data
from household_package.clean import clean_data


df = call_data()
df = clean_data(df)
print(df.head())
