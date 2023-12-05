import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

data = {
    "State" : ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
    ,"Median yearly kWh" : [13300, 6800, 12700, 12200, 5800, 7400, 7200, 10100, 6400, 13100, 12500, 7500, 9700, 7900, 10000, 9300, 10400, 12200, 14000, 6600, 10300, 6600, 7400, 8500, 13200, 11000, 8300, 10000, 10000, 6600, 7900, 7400, 6300, 11800, 10400, 9000, 12100, 9700, 9200, 6800, 12200, 9700, 13000, 12800, 8900, 6400, 11900, 9700, 11200, 7300, 7900]
    ,"1st quartile yearly kWh" : [8900, 4200, 8300, 8600, 3700, 4900, 4500, 7200, 4300, 9000, 8300, 4600, 6600, 5000, 6600, 6300, 6500, 8200, 9800, 4500, 6900, 4500, 5200, 5500, 9400, 7400, 4900, 6300, 7000, 4600, 5300, 4900, 4000, 8000, 6900, 6000, 8200, 6600, 5600, 4400, 8300, 6100, 9500, 8700, 6100, 4100, 7800, 6500, 8100, 5600, 5000]
    ,"3rd quartile yearly kWh" : [17900, 10100, 17800, 17200, 8900, 11200, 10700, 14300, 9600, 18100, 17000, 11300, 14500, 11200, 15300, 13300, 14300, 17700, 18700, 9200, 15600, 10300, 10600, 12000, 18600, 15700, 12800, 14500, 14300, 10100, 11400, 10400, 9700, 15600, 15600, 13700, 18200, 14600, 13600, 9200, 17200, 14700, 18100, 17600, 11700, 9100, 16700, 14300, 18700, 10800, 11700]
    ,"Number of responders" : [242, 311, 495, 268, 1152, 360, 294, 143, 221, 655, 417, 282, 270, 530, 400, 286, 208, 428, 311, 223, 359, 552, 388, 325, 168, 296, 172, 189, 231, 175, 456, 178, 904, 479, 331, 339, 232, 313, 617, 191, 334, 183, 505, 1016, 188, 245, 451, 439, 197, 357, 190]
    ,"Bill" : [1967.0, 1658.0, 1821.0, 1549.0, 1748.0, 1106.0, 2115.0, 1599.0, 1043.0, 2031.0, 1749.0, 3129.0, 1125.0, 1170.0, 1417.0, 1302.0, 1406.0, 1514.0, 1599.0, 1762.0, 1747.0, 1862.0, 1432.0, 1295.0, 1724.0, 1567.0, 1097.0, 1242.0, 1688.0, 1548.0, 1419.0, 1125.0, 1456.0, 1670.0, 1323.0, 1418.0, 1597.0, 1278.0, 1649.0, 1842.0, 1778.0, 1269.0, 1538.0, 1864.0, 1059.0, 1351.0, 1764.0, 1109.0, 1610.0, 1271.0, 993.0]

}

df = pd.DataFrame(data)

df.loc[:,'Monthly kWh'] = round(df['Median yearly kWh']/12,0).astype(int)
df.loc[:,'Monthly bill'] = round(df['Bill']/12,0).astype(int)


for col in df.columns:
    df[col] = df[col].astype(str)

df['text'] = df['State'] + '<br>' + \
    'Monthly kWh: ' + df['Monthly kWh'] + '<br>' + \
    'Respondents: ' + df['Number of responders'] + '<br>' + \
    'Monthly Bill: $' + df['Monthly bill']


st.title('US Electricity Consumption')

# Create a choropleth map using plotly.graph_objects
fig = go.Figure(data=go.Choropleth(
    locations=df['State'],
    z=df['Median yearly kWh'],
    locationmode='USA-states',
    colorscale='Reds',
    colorbar=dict(title='kWh/year'),
    text=df['text'], # hover text
    name=''
))

# Update layout for the map
fig.update_layout(
    title='Average Electricity Consumption per state',
    geo=dict(
        scope='usa',
        projection=go.layout.geo.Projection(type='albers usa'),  # Define the projection
        showlakes=False, # no lakes needed
        lakecolor='rgb(75, 178, 255)',
        bgcolor= 'rgba(0,0,0,0)' #black background
    )
)



#fig.update_traces(
#    hovertemplate="<br>".join([
#        "Avg: %{z} kWh",
#        "Responders: %{customdata['Number of responders']}",
#    ])
#)

st.plotly_chart(fig)
