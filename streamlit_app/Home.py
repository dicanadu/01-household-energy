import streamlit as st

# TODO
# nice image + source
# our names
# link to github repo
# link to data sources

st.set_page_config(page_title='U.S. household electricity consumption'
                   , page_icon='🏠')

# nicer header with html:
st.markdown("<h2 style='text-align: center; color: #CF5050;'> U.S. household electricity consumption </h2>", unsafe_allow_html=True)

# trick to center the image is to assign it to middle column
#with st.columns(3)[1]:
    #st.image('house.jpg', width=300)

st.markdown("<center><img src='https://upload.wikimedia.org/wikipedia/commons/5/54/House_decorated_with_Christmas_lights_at_Moreton_Hall_-_geograph.org.uk_-_1140703.jpg' alt='David Ayrton / Wikimedia' width = 300></center>", unsafe_allow_html=True)


st.markdown('''

:rainbow[Welcome!]

This application will estimate your electrical energy consumption.

''')

st.divider()

st.markdown('''
**Usage:**

:arrow_left: Navigate to 'main' to estimate consumption for your household

:arrow_left: Navigate to 'map' for per-state summary statistics

''')

st.divider()

st.markdown('This project is a part of Le Wagon Data Science bootcamp held in Berlin in October-December 2023.')

st.markdown('Authors: Diego Canales, Richard Kemp, Serkan Sanli, Svetlana Lebedeva.')

st.markdown('[Link to github repository](https://github.com/dicanadu/01-household-energy)')

st.markdown('''
            Data sources:

            - [U.S. residental energy consumption survey](https://www.eia.gov/consumption/residential/data/2020/)

            - [Energybot.com](https://www.energybot.com/electricity-rates-by-state.html#:~:text=The%20Average%20Electricity%20Rate%20in,11.38%20cents%20per%20kilowatt%2Dhour) for electricity price

            ''')

st.markdown('Image source: [David Ayrton / Wikimedia](https://commons.wikimedia.org/wiki/File:House_decorated_with_Christmas_lights_at_Moreton_Hall_-_geograph.org.uk_-_1140703.jpg)')
