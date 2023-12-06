import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(page_title='U.S. wide consumption'
                   , page_icon=':us:')



data = {
    "State" : ['CA', 'NY', 'VT', 'DC', 'ME', 'NH', 'MA', 'AK', 'RI', 'CT', 'WI', 'CO', 'NM', 'MI', 'HI', 'WY', 'NJ', 'IL', 'MT', 'MN', 'UT', 'OH', 'PA', 'IA', 'ID', 'SD', 'OR', 'WA', 'NV', 'NE', 'IN', 'DE', 'MD', 'ND', 'KS', 'MO', 'WV', 'NC', 'VA', 'OK', 'KY', 'AR', 'SC', 'GA', 'AZ', 'TX', 'TN', 'FL', 'MS', 'AL', 'LA']
    ,"Median yearly kWh" : [5800, 6300, 6400, 6400, 6600, 6600, 6600, 6800, 6800, 7200, 7300, 7400, 7400, 7400, 7500, 7900, 7900, 7900, 8300, 8500, 8900, 9000, 9200, 9300, 9700, 9700, 9700, 9700, 10000, 10000, 10000, 10100, 10300, 10400, 10400, 11000, 11200, 11800, 11900, 12100, 12200, 12200, 12200, 12500, 12700, 12800, 13000, 13100, 13200, 13300, 14000]
    ,"Yearly kWh" : ['5,800', '6,300', '6,400', '6,400', '6,600', '6,600', '6,600', '6,800', '6,800', '7,200', '7,300', '7,400', '7,400', '7,400', '7,500', '7,900', '7,900', '7,900', '8,300', '8,500', '8,900', '9,000', '9,200', '9,300', '9,700', '9,700', '9,700', '9,700', '10,000', '10,000', '10,000', '10,100', '10,300', '10,400', '10,400', '11,000', '11,200', '11,800', '11,900', '12,100', '12,200', '12,200', '12,200', '12,500', '12,700', '12,800', '13,000', '13,100', '13,200', '13,300', '14,000']
    ,"Number of responders" : ['1,152', '904', '245', '221', '223', '175', '552', '311', '191', '294', '357', '360', '178', '388', '282', '190', '456', '530', '172', '325', '188', '339', '617', '286', '270', '183', '313', '439', '231', '189', '400', '143', '359', '331', '208', '296', '197', '479', '451', '232', '428', '268', '334', '417', '495', '1,016', '505', '655', '168', '242', '311']
    ,"Monthly bill" : ['146', '121', '113', '87', '147', '129', '155', '138', '154', '176', '106', '92', '94', '119', '261', '83', '118', '98', '91', '108', '88', '118', '137', '108', '94', '106', '106', '92', '141', '104', '118', '133', '146', '110', '117', '131', '134', '139', '147', '133', '126', '129', '148', '146', '152', '155', '128', '169', '144', '164', '133']
    ,"Monthly kWh" : ['486', '522', '531', '534', '547', '554', '554', '564', '570', '602', '612', '613', '615', '617', '628', '655', '656', '659', '693', '706', '745', '753', '763', '773', '808', '810', '811', '812', '830', '836', '838', '842', '858', '864', '870', '918', '933', '987', '994', '1,004', '1,015', '1,019', '1,020', '1,040', '1,055', '1,066', '1,081', '1,091', '1,101', '1,105', '1,170']
    ,"Rank" : ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51']

}

df = pd.DataFrame(data)


for col in df.columns:
    df[col] = df[col].astype(str)

df['text'] = df['State'] + '<br>' + \
    'Yearly kWh: ' + df['Yearly kWh'] + '<br>' + \
    'Monthly kWh: ' + df['Monthly kWh'] + '<br>' + \
    'Monthly Bill: $' + df['Monthly bill'] + '<br>' + \
    'Respondents: ' + df['Number of responders'] + '<br>' + \
    'Rank: ' + df['Rank']



st.markdown("<h2 style='text-align: center; '> U.S. electricity consumption statistics </h2>", unsafe_allow_html=True)


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

st.markdown('''
            Hover over the state to show:
            - yearly consumption per state (kWh)
            - monthly consumption per state (kWh)
            - monthly average electricity bill
            - number of respondents to the survey
            - the rank of the state by electricity consumption (1 = lowest)
            ''')
