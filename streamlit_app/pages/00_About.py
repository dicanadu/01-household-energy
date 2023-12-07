import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import os

st.set_page_config(page_title='About'
                   , page_icon=':computer:')

# nicer header with html:
st.markdown("<h2 style='text-align: center;'> How does our app work? </h2>", unsafe_allow_html=True)


st.markdown('''

:green[**About the dataset!**]

The data is retrieved from the residential energy consumption survey 2020 conducted by the :green[**Energy Information Administration (EIA)**].

''')

st.markdown('''

It's a representative sample of :green[**18,500 Housing units**] combined with energy suppliers information.

''')

st.divider()

st.markdown('''
:green[**Model dataflow**] '''
)

file_path = os.path.join(os.path.dirname(__file__), "images","household_energy_flowchart.png")
flowchart_img = Image.open(file_path)
st.image(flowchart_img)

st.divider()

st.markdown('''

:green[**About the model!**]

The base model is a :green[**Linear Regression!**] on selected features, which were:
 - Cleaned (Outliers, Missing values, Imputation)
 - Preprocessed (Feature Engineering, MinMaxScaler, StandardScaler, OneHotEncoder)
 - Tuned (Adjusting parameters)
 - Fitted
''')

st.markdown('''

The model uses the following features:

''')

columns = st.columns(3)

vars = [ "state_name", "BA_climate", "TYPEHUQ", "STORIES", "YEARMADERANGE", "NCOMBATH", "NHAFBATH", "TOTROOMS",  "WINDOWS",
           "SWIMPOOL", "NUMFRIG", "MICRO", "DISHWASH", "CWASHER", "DRYER", "TVCOLOR", "DESKTOP", "NUMLAPTOP",
           "HEATHOME", "EQUIPM", "NUMPORTEL", "AIRCOND", "LGTIN1TO4", "LGTIN4TO8", "LGTINMORE8",  "NHSLDMEM", "SQFTEST",
          "KWH", "DOLLAREL"]

html_1 = """<ul>
    <li>State</li>
    <li>House area (squared foot)</li>
    <li>Price per kWh</li>
    <li>Year of construction</li>
    <li>Type of climate</li>
    <li>Type of household</li>
    <li>Type of heating system</li>
    <li>Has a washing maschine?</li>
    <li>Has a clothes dryer?</li>
</ul> """

html_2 = """<ul>
    <li>Has heating system?</li>
    <li>Has air conditioner?</li>
    <li>Has a swimming pool?</li>
    <li>Has a dishwasher?</li>
    <li>Number of household members</li>
    <li>Number of rooms</li>
    <li>Number of bathrooms</li>
    <li>Number of stories</li>
</ul> """

html_3 = """<ul>
    <li>Number of windows</li>
    <li>Number of refrigerators</li>
    <li>Number of microwaves</li>
    <li>Number of tvs</li>
    <li>Number of electric heaters</li>
    <li>Number of tvs</li>
    <li>Number of computers</li>
    <li>Number of lighting bulbs</li>

</ul> """

columns[0].markdown(html_1, unsafe_allow_html=True)
columns[1].markdown(html_2, unsafe_allow_html=True)
columns[2].markdown(html_3, unsafe_allow_html=True)

st.divider()

st.markdown('''
:green[**About the API!**] '''
)

st.markdown('''

Finally for predictions, pass the below parameters to our [API](https://us-electricity-estimator-jaiabuy6eq-ew.a.run.app/predict)

Call our API and try it yourself !!!!

: )
''')

variable = ['TYPEHUQ', 'NHSLDMEM', 'state_name', 'BA_climate', 'SQFTEST',
       'STORIES', 'YEARMADERANGE', 'NCOMBATH', 'NHAFBATH', 'TOTROOMS',
       'WINDOWS', 'SWIMPOOL', 'SMARTMETER', 'DESKTOP', 'NUMLAPTOP',
       'TVCOLOR', 'DISHWASH', 'MICRO', 'NUMFRIG', 'CWASHER', 'DRYER',
       'LGTIN1TO4', 'LGTIN4TO8', 'LGTINMORE8', 'AIRCOND', 'EQUIPM',
       'HEATHOME', 'NUMPORTEL']
description = ['Type of housing unit', 'Number of household members',
       'State Name', 'Building America Climate Zone',
       'Respondent-reported square footage (rounded to the nearest 10)',
       'Number of stories in a single-family home',
       'Range when housing unit was built',
       'Number of full bathrooms',
       'Number of half bathrooms',
       'Total number of rooms in the housing unit, excluding bathrooms; a derived variable',
       'Number of windows', 'Has swimming pool',
       'Home has an electricity smart meter',
       'Number of desktop computers used',
       'Number of laptop computers used', 'Number of televisions used',
       'Has dishwasher', 'Number of microwaves',
       'Number of refrigerators used', 'Has clothes washer in home',
       'Has clothes dryer in home',
       'Number of inside light bulbs turned on 1 to 4 hours per day',
       'Number of inside light bulbs turned on 4 to 8 hours per day',
       'Number of inside light bulbs turned on more than 8 hours per day',
       'Air conditioning equipment used',
       'Main space heating equipment type',
       'Space heating equipment used',
       'Number of portable electric heaters used']
data_type = [' int', ' int', ' str', ' str', ' int', ' int', ' int', ' int',
       ' int', ' int', ' int', ' int', ' int', ' int', ' int', ' int',
       ' int', ' int', ' int', ' int', ' int', ' int', ' int', ' int',
       ' int', ' int', ' int', ' int']
example = ['1 Mobile home\n2 Single-family house detached from any other house \n3 Single-family house attached to one or more other houses (for example: duplex, row house, or townhome)\n4 Apartment in a building with 2 to 4 units\n5 Apartment in a building with 5 or more units',
       '1 - 7', 'Alaska - Wyoming ',
       'Cold\nHot-Dry\nHot-Humid\nMarine\nMixed-Dry\nMixed-Humid\nSubarctic\nVery-Cold',
       '240-15000',
       '1 One story\n2 Two stories\n3 Three stories\n4 Four or more stories\n5 Split-level\n-2 Not applicable',
       '1 Before 1950\n2 1950 to 1959\n3 1960 to 1969\n4 1970 to 1979\n5 1980 to 1989\n6 1990 to 1999\n7 2000 to 2009\n8 2010 to 2015\n9 2016 to 2020',
       '0 - 4', '0 - 2', '1-15',
       '1 1 or 2 windows\n2 3 to 5 windows\n3 6 to 9 windows\n4 10 to 15 windows\n5 16 to 19 windows\n6 20 to 29 windows\n7 30 or more windows',
       '1 Yes\n0 No\n-2 Not applicable', "1 Yes\n0 No\n-4 Don't Know",
       '0 - 8', '0 - 20', '0 - 14', '1 Yes\n0 No', '0 - 3', '0 - 9',
       '1 Yes\n0 No', '1 Yes\n0 No', '0 - 90', '0 - 84', '0 - 99',
       '1 Yes\n0 No',
       '3 Central furnace \n2 Steam or hot water system with radiators or pipes \n4 Central heat pump\n13 Ductless heat pump, also known as a "mini-split"\n5 Built-in electric units installed in walls, ceilings, baseboards, or floors\n7 Built-in room heater burning gas or oil\n8 Wood or pellet stove \n10 Portable electric heaters\n99 Other \n-2 Not applicable',
       '1 Yes\n0 No', '1 - 9\n-2 Not applicable']
variable_df = pd.DataFrame({"variable": variable, "description": description, 'data_type': data_type, 'codes': example}).set_index("variable")
variable_df.index.name = None

# Set Streamlit option to display all rows
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
df_2 = pd.DataFrame(user_input, index = [0]).T
converged_pd = pd.merge(variable_df, df_2, left_index=True, right_index=True)
converged_pd.columns = ["Description", "Data Type", "Codes", "Example"]

st.dataframe(converged_pd)
