from household_package.data import call_data_url
from household_package.data import call_data_cloud
from household_package.clean import clean_data


df = call_data_url()
#df2 = call_data_cloud()
df2 = clean_data(df)
print(df2.head())
