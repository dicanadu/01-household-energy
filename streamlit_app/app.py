import requests
import streamlit as st

'''
# U.S. Household Energy Consumption
# 🇺🇸🏠


This application will estimate your yearly energy consumption in kwh.

'''

########### hard-coded constants ###############

# U.S. states selector
states=('Alabama',
 'Alaska',
 'Arizona',
 'Arkansas',
 'California',
 'Colorado',
 'Connecticut',
 'Delaware',
 'District of Columbia',
 'Florida',
 'Georgia',
 'Hawaii',
 'Idaho',
 'Illinois',
 'Indiana',
 'Iowa',
 'Kansas',
 'Kentucky',
 'Louisiana',
 'Maine',
 'Maryland',
 'Massachusetts',
 'Michigan',
 'Minnesota',
 'Mississippi',
 'Missouri',
 'Montana',
 'Nebraska',
 'Nevada',
 'New Hampshire',
 'New Jersey',
 'New Mexico',
 'New York',
 'North Carolina',
 'North Dakota',
 'Ohio',
 'Oklahoma',
 'Oregon',
 'Pennsylvania',
 'Rhode Island',
 'South Carolina',
 'South Dakota',
 'Tennessee',
 'Texas',
 'Utah',
 'Vermont',
 'Virginia',
 'Washington',
 'West Virginia',
 'Wisconsin',
 'Wyoming')



############### user input ##################

state = st.selectbox('Select your state:', states)

st.slider('Number of persons in your household:', 1, 7, 1)

st.number_input('Estimated area of your house in sq.feet:',
                min_value=100, max_value=None, value="min", step=10)


############### API ###########################

# API:
#params={}
#url=
#response=requests.get(url,params=params).json()

#output prediction:
#pred_kwh=response.get('y_pred')

# dummy prediciton - actual median of the dataset
pred_kwh=9346.435000000001


############# callback to calculate kWh ################

if st.button('Estimate my consumption'):
    st.write(f'''
             Your estimated consumption:\n
             {pred_kwh:.1f} kWh''')
