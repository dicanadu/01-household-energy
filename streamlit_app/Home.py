import streamlit as st
from datetime import datetime

# Get the current date
current_date = datetime.now()

st.set_page_config(page_title='U.S. household electricity consumption'
                   , page_icon='🏠')

# nicer header with html: #CF5050
st.markdown("<h2 style='text-align: center; '> 🌩️ U.S. household electricity consumption 💡 </h2>", unsafe_allow_html=True)

# Check if the month is November or December
if current_date.month in [11, 12]:
    image_url = 'https://upload.wikimedia.org/wikipedia/commons/5/54/House_decorated_with_Christmas_lights_at_Moreton_Hall_-_geograph.org.uk_-_1140703.jpg'
    author_ref = 'David Ayrton / Wikimedia'
    st.markdown(f"<center><img src='{image_url}' alt='{author_ref}' width = 300></center>", unsafe_allow_html=True)
else:
    image_url = 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a1/Las_Vegas_%28Nevada%2C_USA%29%2C_The_Strip_--_2012_--_6232.jpg/320px-Las_Vegas_%28Nevada%2C_USA%29%2C_The_Strip_--_2012_--_6232.jpg'
    author_ref = 'Dietmar Rabich / Wikimedia'
    st.markdown(f"<center><img src='{image_url}' alt='{author_ref}' width = 300></center>", unsafe_allow_html=True)

st.markdown('''

:rainbow[Welcome!]

Living in or moving to the U.S.? Planning to buy a house? Wondering about your electricity bill?

This application will estimate your electrical energy consumption!

''')

st.divider()

st.markdown('''
**Usage:**

:arrow_left: Navigate to [Electricity Estimator](https://us-electricity-calculator.streamlit.app/Electricity_Estimator) to estimate consumption for your household

:arrow_left: Navigate to [US Consumption](https://us-electricity-calculator.streamlit.app/US_Consumption) for per-state summary statistics

''')

st.divider()

st.markdown('This project is a part of Le Wagon Data Science bootcamp held in Berlin in October-December 2023')

st.markdown('''
            Data sources:

            - [U.S. residental energy consumption survey](https://www.eia.gov/consumption/residential/data/2020/)

            - [Energybot.com](https://www.energybot.com/electricity-rates-by-state.html#:~:text=The%20Average%20Electricity%20Rate%20in,11.38%20cents%20per%20kilowatt%2Dhour) for electricity price

            ''')

st.markdown(f'Image source: [{author_ref}]({image_url})')

st.subheader('Authors: [Diego Canales](https://www.linkedin.com/in/diego-canales-794564a1/), [Richard Kemp](https://www.linkedin.com/in/richard-kemp-432851163/), [Serkan Sanli](https://www.linkedin.com/in/serkan-sanli-6a0861257/), [Svetlana Lebedeva](https://www.linkedin.com/in/svetlana-lebedeva-7b400110a/)')

st.markdown('[Link to github repository](https://github.com/dicanadu/01-household-energy)')
