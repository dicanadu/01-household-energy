import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

data = {
    "State" : ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
    ## int: to plot
    ,"Median yearly kWh" : [13300, 6800, 12700, 12200, 5800, 7400, 7200, 10100, 6400, 13100, 12500, 7500, 9700, 7900, 10000, 9300, 10400, 12200, 14000, 6600, 10300, 6600, 7400, 8500, 13200, 11000, 8300, 10000, 10000, 6600, 7900, 7400, 6300, 11800, 10400, 9000, 12100, 9700, 9200, 6800, 12200, 9700, 13000, 12800, 8900, 6400, 11900, 9700, 11200, 7300, 7900]
    ## string: to show in hovertext
    ,"Yearly kWh" : ['13,300', '6,800', '12,700', '12,200', '5,800', '7,400', '7,200', '10,100', '6,400', '13,100', '12,500', '7,500', '9,700', '7,900', '10,000', '9,300', '10,400', '12,200', '14,000', '6,600', '10,300', '6,600', '7,400', '8,500', '13,200', '11,000', '8,300', '10,000', '10,000', '6,600', '7,900', '7,400', '6,300', '11,800', '10,400', '9,000', '12,100', '9,700', '9,200', '6,800', '12,200', '9,700', '13,000', '12,800', '8,900', '6,400', '11,900', '9,700', '11,200', '7,300', '7,900']
    ,"Number of responders" : ['242', '311', '495', '268', '1,152', '360', '294', '143', '221', '655', '417', '282', '270', '530', '400', '286', '208', '428', '311', '223', '359', '552', '388', '325', '168', '296', '172', '189', '231', '175', '456', '178', '904', '479', '331', '339', '232', '313', '617', '191', '334', '183', '505', '1,016', '188', '245', '451', '439', '197', '357', '190']
    ,"Monthly bill" : ['164', '138', '152', '129', '146', '92', '176', '133', '87', '169', '146', '261', '94', '98', '118', '108', '117', '126', '133', '147', '146', '155', '119', '108', '144', '131', '91', '104', '141', '129', '118', '94', '121', '139', '110', '118', '133', '106', '137', '154', '148', '106', '128', '155', '88', '113', '147', '92', '134', '106', '83']
    ,"Monthly kWh" : ['1,105', '564', '1,055', '1,019', '486', '613', '602', '842', '534', '1,091', '1,040', '628', '808', '659', '838', '773', '870', '1,015', '1,170', '547', '858', '554', '617', '706', '1,101', '918', '693', '836', '830', '554', '656', '615', '522', '987', '864', '753', '1,004', '811', '763', '570', '1,020', '810', '1,081', '1,066', '745', '531', '994', '812', '933', '612', '655']


}

df = pd.DataFrame(data)


for col in df.columns:
    df[col] = df[col].astype(str)

df['text'] = df['State'] + '<br>' + \
    'Yearly kWh: ' + df['Yearly kWh'] + '<br>' + \
    'Monthly kWh: ' + df['Monthly kWh'] + '<br>' + \
    'Monthly Bill: $' + df['Monthly bill'] + '<br>' + \
    'Respondents: ' + df['Number of responders'] #+ '<br>' + \



st.markdown("<h2 style='text-align: center; '> U.S. electricity consumption statistics </h2>", unsafe_allow_html=True)

#st.title('US Electricity Consumption')

# Create a choropleth map using plotly.graph_objects
fig = go.Figure(data=go.Choropleth(
    locations=df['State'],
    z=df['Median yearly kWh'],
    locationmode='USA-states',
    # colorscale='Bergeron',
    # colorscale='thermal',
    colorscale='portland',
    colorbar=dict(title='kWh/year'),
    hovertext=df['text'], # hover text
    hoverinfo='text',
    #hoverlabel=#dict for text,bgcolor
    name=''
))

# Update layout for the map
fig.update_layout(
    #title='Average Electricity Consumption per state',
    geo=dict(
        scope='usa',
        projection=go.layout.geo.Projection(type='albers usa'),  # Define the projection
        showlakes=False, # no lakes needed
        lakecolor='rgb(75, 178, 255)',
        bgcolor= 'rgba(0,0,0,0)' #black backgrounds
        # bgcolor='rgba(0,0,255,0)'  # semi-transparent black background
    )
)



#fig.update_traces(
#    hovertemplate="<br>".join([
#        "Avg: %{z} kWh",
#        "Responders: %{customdata['Number of responders']}",
#    ])
#)

st.plotly_chart(fig)
