import requests
import streamlit as st
import pandas as pd


############# functions ############

def make_selectbox(feature):
    '''
    Take a feature that needs a dropdown selector
    Returns a tuple of ('label',['option1','option2'])
    Which is an input to streamlit checkbox
    '''
    label = label_dict.get(feature)
    dropdown_list = values_dict.get(feature).split('\n')

    return label,dropdown_list


'''
# U.S. Household Energy Consumption
# 🇺🇸🏠


This application will estimate your yearly energy consumption in kwh.

'''

############### API ###########################

# API:
params={}
#url=
#response=requests.get(url,params=params).json()

#output prediction:
#pred_kwh=response.get('y_pred')

# dummy prediciton - actual median of the dataset
pred_kwh=9346.435000000001



########### hard-coded constants ###############

# selected features
selected = pd.read_csv('selected_features.csv', index_col=0)

# make a dictionary to select features
val_cols = ['Description and Labels','Response Codes']
key_col=['Variable']
label_dict = selected.set_index(key_col)[val_cols[0]].to_dict()
values_dict = selected.set_index(key_col)[val_cols[1]].to_dict()

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

#STORIES = st.slider('How many stories does your house have?', min_value=1, max_value=5, value=2)

your_home = 'TYPEHUQ','STORIES','YEARMADERANGE','NCOMBATH','NHAFBATH','TOTROOMS','WALLTYPE','ROOFTYPE','WINDOWS','SWIMPOOL','SQFTEST'

#home_explained =
#home_dict = {k:v for k,v in zip(your_home, home_explained)}
#for param in your_home:    st.number_input(param)

##### features that need a dropdown #####

selectbox_features = selected['Variable'][selected['Response Codes'].str.contains('\n')].to_list()
selectbox_features.remove('REGIONC') # will be derived from state code
for feat in selectbox_features:
    params[feat] = make_selectbox(feat)


##### features with numeric input #####

numeric_features = selected['Variable'][selected['Response Codes'].str.match('[0-9]+\s*-\s*[0-9]+$')]
for feat in numeric_features:
    params[feat] = st.number_input(label=label_dict.get(feat))

###### section HOUSEHOLD CHARACTERISTICS ######

NHSLDMEM = st.slider('Number of persons in your household:', 1, 7, 2)

SQFTEST = st.number_input('Estimated area of your house in sq.feet:',
                min_value=100, max_value=None, value=1500, step=10)






############# callback to calculate kWh ################

if st.button('Estimate my consumption'):
    st.write(f'''
             Your estimated consumption:\n
             {pred_kwh:.1f} kWh''')
