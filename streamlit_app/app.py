import requests
import streamlit as st
import pandas as pd

########## page info ############

st.set_page_config(page_title='U.S. household electricity consumption'
                   , page_icon='🏠')




'''
# U.S. Household Energy Consumption
# 🇺🇸🏠


This application will estimate your yearly energy consumption (in kWh).

'''

############### API ###########################

# API:
params={}

## test of the API to docker container on the cloud
test_params = {'state_name': 'TX'}
url='https://householdpredictions-jaiabuy6eq-ew.a.run.app/predict'

#@st.cache_data(ttl=3600) # cache data for 1 hour
def api_call(url, params):
    response=requests.get(url,params).json()
    #output prediction:
    return response.get("kwh_prediction")


########### hard-coded constants ###############

label_dict = {'REGIONC': 'Census Region',
 'state_name': 'State Name',
 'BA_climate': 'Building America Climate Zone',
 'IECC_climate_code': '2012 International Energy Conservation Code climate code',
 'TYPEHUQ': 'Type of housing unit',
 'STORIES': 'Number of stories in a single-family home',
 'YEARMADERANGE': 'Range when housing unit was built',
 'NCOMBATH': 'Number of full bathrooms (top-coded)',
 'NHAFBATH': 'Number of half bathrooms (top-coded)',
 'TOTROOMS': 'Total number of rooms in the housing unit, excluding bathrooms; a derived variable',
 'WALLTYPE': 'Major outside wall material',
 'ROOFTYPE': "Major roofing material; 'Not applicable' applies to apartment buildings with 5 or more units",
 'WINDOWS': 'Number of windows',
 'SWIMPOOL': 'Has swimming pool',
 'NUMFRIG': 'Number of refrigerators used',
 'MICRO': 'Number of microwaves',
 'DISHWASH': 'Has dishwasher',
 'CWASHER': 'Has clothes washer in home',
 'DRYER': 'Has clothes dryer in home',
 'TVCOLOR': 'Number of televisions used',
 'DESKTOP': 'Number of desktop computers used',
 'NUMLAPTOP': 'Number of laptop computers used',
 'TELLWORK': 'Any household member teleworking',
 'TELLDAYS': 'Number of days teleworking in the past week',
 'HEATHOME': 'Space heating equipment used',
 'EQUIPM': 'Main space heating equipment type',
 'NUMPORTEL': 'Number of portable electric heaters used',
 'AIRCOND': 'Air conditioning equipment used',
 'NUMPORTAC': 'Number of portable air conditioners used',
 'LGTIN1TO4': 'Number of inside light bulbs turned on 1 to 4 hours per day',
 'LGTIN4TO8': 'Number of inside light bulbs turned on 4 to 8 hours per day',
 'LGTINMORE8': 'Number of inside light bulbs turned on more than 8 hours per day',
 'SMARTMETER': 'Home has an electricity smart meter',
 'SOLAR': "On-site electricity generation from solar; 'Not applicable' applies to apartment buildings with 2 or more units.",
 'NHSLDMEM': 'Number of household members (top-coded)',
 'SQFTEST': 'Respondent-reported square footage (rounded to the nearest 10)'}

values_dict = {'REGIONC': 'Midwest\nNortheast\nSouth\nWest',
 'state_name': 'state_dictionary!A1',
 'BA_climate': 'Cold\nHot-Dry\nHot-Humid\nMarine\nMixed-Dry\nMixed-Humid\nSubarctic\nVery-Cold',
 'IECC_climate_code': '1A\n2A\n2B\n3A\n3B\n3C\n4A\n4B\n4C\n5A\n5B\n5C\n6A\n6B\n7A\n7AK\n7B\n8AK',
 'TYPEHUQ': '1 Mobile home\n2 Single-family house detached from any other house \n3 Single-family house attached to one or more other houses (for example: duplex, row house, or townhome)\n4 Apartment in a building with 2 to 4 units\n5 Apartment in a building with 5 or more units',
 'STORIES': '1 One story\n2 Two stories\n3 Three stories\n4 Four or more stories\n5 Split-level\n-2 Not applicable',
 'YEARMADERANGE': '1 Before 1950\n2 1950 to 1959\n3 1960 to 1969\n4 1970 to 1979\n5 1980 to 1989\n6 1990 to 1999\n7 2000 to 2009\n8 2010 to 2015\n9 2016 to 2020',
 'NCOMBATH': '0 - 4',
 'NHAFBATH': '0 - 2',
 'TOTROOMS': '1-15',
 'WALLTYPE': '1 Brick\n2 Wood\n3 Siding (aluminum, fiber cement, vinyl, or steel) \n4 Stucco\n5 Shingle (composition)\n6 Stone \n7 Concrete block \n99 Other',
 'ROOFTYPE': '1 Ceramic or clay tiles\n2 Wood shingles/shakes\n3 Metal\n4 Slate or synthetic slate\n5 Shingles (composition or asphalt)\n6 Concrete tiles\n99 Other\n-2 Not applicable',
 'WINDOWS': '1 1 or 2 windows\n2 3 to 5 windows\n3 6 to 9 windows\n4 10 to 15 windows\n5 16 to 19 windows\n6 20 to 29 windows\n7 30 or more windows',
 'SWIMPOOL': '1 Yes\n0 No\n-2 Not applicable',
 'NUMFRIG': '0 - 9',
 'MICRO': '0 - 3',
 'DISHWASH': '1 Yes\n0 No',
 'CWASHER': '1 Yes\n0 No',
 'DRYER': '1 Yes\n0 No',
 'TVCOLOR': '0 - 14',
 'DESKTOP': '0 - 8',
 'NUMLAPTOP': '0 - 20',
 'TELLWORK': '1 Yes\n0 No',
 'TELLDAYS': '0 - 7\n-2  Not applicable',
 'HEATHOME': '1 Yes\n0 No',
 'EQUIPM': '3 Central furnace \n2 Steam or hot water system with radiators or pipes \n4 Central heat pump\n13 Ductless heat pump, also known as a “mini-split”\n5 Built-in electric units installed in walls, ceilings, baseboards, or floors\n7 Built-in room heater burning gas or oil\n8 Wood or pellet stove \n10 Portable electric heaters\n99 Other \n-2 Not applicable',
 'NUMPORTEL': '1 - 9\n-2 Not applicable',
 'AIRCOND': '1 Yes\n0 No',
 'NUMPORTAC': '1 - 8\n-2 Not applicable',
 'LGTIN1TO4': '0 - 90',
 'LGTIN4TO8': '0 - 84',
 'LGTINMORE8': '0 - 99',
 'SMARTMETER': "1 Yes\n0 No\n-4 Don't Know",
 'SOLAR': '1 Yes\n0 No\n-2 Not applicable',
 'NHSLDMEM': '1 - 7',
 'SQFTEST': '240-15000'}

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

# TODO state to region


########## separate features by type ##############

geo_features = ['state_name']#, 'REGIONC']
selectbox_features = ['BA_climate', 'IECC_climate_code']
numeric_features = ['NCOMBATH', 'NHAFBATH', 'TOTROOMS', 'NUMFRIG', 'MICRO', 'TVCOLOR', 'DESKTOP', 'NUMLAPTOP', 'LGTIN1TO4', 'LGTIN4TO8', 'LGTINMORE8', 'NHSLDMEM', 'SQFTEST']
num_checkbox_features = ['TYPEHUQ', 'STORIES', 'YEARMADERANGE', 'WALLTYPE', 'ROOFTYPE', 'WINDOWS', 'SWIMPOOL', 'DISHWASH', 'CWASHER', 'DRYER', 'TELLWORK', 'HEATHOME', 'EQUIPM', 'AIRCOND', 'SMARTMETER', 'SOLAR']
numeric_features_dropdown = ['TELLDAYS', 'NUMPORTEL', 'NUMPORTAC']
all_features = geo_features+numeric_features+num_checkbox_features+numeric_features_dropdown#+selectbox_features
########### dictionary of mappings ################

mapped_features={}
for feature in num_checkbox_features:
    mapped_features[feature]=dict(val.split(' ', 1)[::-1] for val in values_dict.get(feature).split('\n'))
for feature in numeric_features_dropdown:
    str_range, text  = values_dict[feature].split('\n')
    d = {str(k):str(k) for k in range(int(str_range.split(' - ')[-1])+1)}
    d.update({text.split(' ',1)[1]:text.split(' ',1)[0]})
    mapped_features[feature] = d


############# functions ############

@st.cache_data
def make_numeric_input(feature):
    label = label_dict.get(feature)
    min_value, max_value = (int(val) for val in values_dict.get(feature).split('-'))
    return label, min_value, max_value

def record_user_input(feature):
    """
    This function creates an input widget for a feature
    Depending on which type the feature is.
    It will write the user input value into params dictionary.
    """
    ##### geography features ######
    if feature=='state_name':
        state_postal = st.selectbox('Select your state:', states.keys())
        params['state_name'] = states.get(state_postal)
    # TODO derive region from state name 'REGIONC'


    ##### features that need a dropdown text #####
    if feature in selectbox_features:
        params[feature] = st.selectbox(label = label_dict.get(feature),
                                    options= values_dict.get(feature).split('\n'))
    ##### features with purely numeric input #####
    if feature in numeric_features:
        params[feature] = int(st.number_input(*make_numeric_input(feature)))

    ##### features where dropdown input is transferred to numeric #####
    if feature in num_checkbox_features:
        user_value = st.selectbox(label=label_dict.get(feature),
                                  options=mapped_features.get(feature).keys())
        params[feature] = int(mapped_features.get(feature).get(user_value))

    ##### features which have both numeric range and text #####
    if feature in numeric_features_dropdown:
        user_value = st.selectbox(label=label_dict.get(feature),
                                  options=mapped_features.get(feature).keys())
        params[feature] = int(mapped_features.get(feature).get(user_value))



############## tabs - organize features by sections ###############

tab_main, tab_household, tab_appliances = st.tabs(['About your home',
                                                   'Household characteristics',
                                                    'Applicances'])

#############################################
############### user input ##################
#############################################

###### section Main: GEOGRAPHY, ADMIN, basic household (type, no. of persons) ##########

with tab_main:
    st.subheader('About your home')

    main_features = ['TYPEHUQ','NHSLDMEM', 'state_name']
    for feature in main_features:
        record_user_input(feature)


    ###### section ADMIN ######
    # right now don't know how to input climate or climate code as a user


with tab_household:
    st.subheader('Your household')

    ###### section HOUSEHOLD CHARACTERISTICS ######

    household_features = ['SQFTEST', 'STORIES','YEARMADERANGE','NCOMBATH',
 'NHAFBATH','TOTROOMS', 'WALLTYPE','ROOFTYPE','WINDOWS', 'SWIMPOOL',
 'SMARTMETER']
    for feature in household_features:
        record_user_input(feature)


with tab_appliances:
    st.subheader('Applicances')

    appliance_features = list(set(all_features).difference(
        set(main_features+household_features)))
    for feature in appliance_features:
        record_user_input(feature)



### Parameters sent to the API:
    #st.write(params)



############# callback to calculate kWh ################

if st.button('Estimate my consumption'):
    pred_kwh = api_call(url, params=test_params)
    st.write(f'''
             Your estimated consumption:\n
             {pred_kwh} kWh''')
