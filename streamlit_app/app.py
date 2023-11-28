import requests
import streamlit as st
import pandas as pd


############# functions ############




'''
# U.S. Household Energy Consumption
# 🇺🇸🏠


This application will estimate your yearly energy consumption in kwh.

'''

############### API ###########################

# API:
params={}

## test of the API to docker container on the cloud
test_params = {'state_name': 'TX'}
url='https://householdpredictions-jaiabuy6eq-ew.a.run.app/predict'
response=requests.get(url,params=test_params).json()

#output prediction:
pred_kwh=response.get("kwh_prediction")

# dummy prediciton - actual median of the dataset
#pred_kwh=9346.435000000001



########### hard-coded constants ###############

# selected features
selected = pd.read_csv('selected_features.csv', index_col=0)

# make a dictionary to select features
val_cols = ['Description and Labels','Response Codes']
key_col=['Variable']
label_dict = selected.set_index(key_col)[val_cols[0]].to_dict()
values_dict = selected.set_index(key_col)[val_cols[1]].to_dict()

# sections
sections = list(selected.Section.unique())

# U.S. states selector
states = {'AL': 'Alabama',
 'AK': 'Alaska',
 'AZ': 'Arizona',
 'AR': 'Arkansas',
 'CA': 'California',
 'CO': 'Colorado',
 'CT': 'Connecticut',
 'DE': 'Delaware',
 'DC': 'District of Columbia',
 'FL': 'Florida',
 'GA': 'Georgia',
 'HI': 'Hawaii',
 'ID': 'Idaho',
 'IL': 'Illinois',
 'IN': 'Indiana',
 'IA': 'Iowa',
 'KS': 'Kansas',
 'KY': 'Kentucky',
 'LA': 'Louisiana',
 'ME': 'Maine',
 'MD': 'Maryland',
 'MA': 'Massachusetts',
 'MI': 'Michigan',
 'MN': 'Minnesota',
 'MS': 'Mississippi',
 'MO': 'Missouri',
 'MT': 'Montana',
 'NE': 'Nebraska',
 'NV': 'Nevada',
 'NH': 'New Hampshire',
 'NJ': 'New Jersey',
 'NM': 'New Mexico',
 'NY': 'New York',
 'NC': 'North Carolina',
 'ND': 'North Dakota',
 'OH': 'Ohio',
 'OK': 'Oklahoma',
 'OR': 'Oregon',
 'PA': 'Pennsylvania',
 'RI': 'Rhode Island',
 'SC': 'South Carolina',
 'SD': 'South Dakota',
 'TN': 'Tennessee',
 'TX': 'Texas',
 'UT': 'Utah',
 'VT': 'Vermont',
 'VA': 'Virginia',
 'WA': 'Washington',
 'WV': 'West Virginia',
 'WI': 'Wisconsin',
 'WY': 'Wyoming'}






############### user input ##################




###### section GEOGRAPHY ##########

'''
### Your location
'''

state_postal = st.selectbox('Select your state:', states.keys())
state_name = states.get(state_postal)

# TODO derive region from state name 'REGIONC'


###### section ADMIN ######


# right now don't know how to input climate or climate code

####### section YOUR HOME #######

'''
### Your home
'''


##### features that need a dropdown #####

#selectbox_features = selected['Variable'][selected['Response Codes'].str.contains('\n')].to_list()
#selectbox_features.remove('REGIONC') # will be derived from state code

selectbox_features = ['BA_climate', 'IECC_climate_code']
for feature in selectbox_features:
    params[feature] = st.selectbox(label = label_dict.get(feature),
                                options= values_dict.get(feature).split('\n'))


##### features with purely numeric input #####

numeric_features = ['NCOMBATH', 'NHAFBATH', 'TOTROOMS', 'NUMFRIG', 'MICRO', 'TVCOLOR', 'DESKTOP', 'NUMLAPTOP', 'LGTIN1TO4', 'LGTIN4TO8', 'LGTINMORE8', 'NHSLDMEM', 'SQFTEST']
for feat in numeric_features:
    params[feat] = st.number_input(label=label_dict.get(feat))


##### features where dropdown input is transferred to numeric #####

#num_checkbox_features = selected['Variable'][ (selected['Response Codes'].str.contains('\n')) & (selected['Type']=='Num')].to_list()

num_checkbox_features = ['TYPEHUQ', 'STORIES', 'YEARMADERANGE', 'WALLTYPE', 'ROOFTYPE', 'WINDOWS', 'SWIMPOOL', 'DISHWASH', 'CWASHER', 'DRYER', 'TELLWORK', 'TELLDAYS', 'HEATHOME', 'EQUIPM', 'NUMPORTEL', 'AIRCOND', 'NUMPORTAC', 'SMARTMETER', 'SOLAR']
mapped_features={}
for feature in num_checkbox_features:
    mapped_features[feature]=dict(val.split(' ', 1)[::-1] for val in values_dict.get(feature).split('\n'))


#for feature in num_checkbox_features:
#    st.selectbox(label = label_dict.get(feature),
#                 options = )


###### section HOUSEHOLD CHARACTERISTICS ######

NHSLDMEM = st.slider('Number of persons in your household:', 1, 7, 2)

SQFTEST = st.number_input('Estimated area of your house in sq.feet:',
                min_value=100, max_value=None, value=1500, step=10)


st.write(params)



############# callback to calculate kWh ################

if st.button('Estimate my consumption'):
    st.write(f'''
             Your estimated consumption:\n
             {pred_kwh} kWh''')
