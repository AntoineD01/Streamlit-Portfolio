import streamlit as st
import pandas as pd
from streamlit_folium import folium_static
import plotly.express as px
import plotly.graph_objects as go

@st.cache_data
def load_data():
    data = pd.read_csv('cars.csv', delimiter=',')  
    data.columns = data.columns.str.strip()  # Strip whitespace from column names
    return data
    
data = load_data()

st.title('Electric Vehicle Dataset')
st.write('This dataset contains information about electric vehicles and non-electric vehicles in France.')

#Cleaning the data
#We convert codgeo to int and delete corsica
data['codgeo'] = data['codgeo'].astype(str)

data = data[~data['codgeo'].str.startswith('2A')]
data = data[~data['codgeo'].str.startswith('2B')]

data['codgeo'] = data['codgeo'].astype(int)

#We convert date_arrete to datetime
data['date_arrete'] = pd.to_datetime(data['date_arrete'])

# Extract the year from date_arrete
data['year'] = data['date_arrete'].dt.year

# Extract the department from the 'codgeo' column (first two digits)
data['department'] = data['codgeo'].astype(str).str[:2]

# Create a dictionary to map departments to regions
dept_to_region = {
    '01': 'Auvergne-Rhône-Alpes', '03': 'Auvergne-Rhône-Alpes', '07': 'Auvergne-Rhône-Alpes', '15': 'Auvergne-Rhône-Alpes',
    '26': 'Auvergne-Rhône-Alpes', '38': 'Auvergne-Rhône-Alpes', '42': 'Auvergne-Rhône-Alpes', '43': 'Auvergne-Rhône-Alpes',
    '63': 'Auvergne-Rhône-Alpes', '69': 'Auvergne-Rhône-Alpes', '73': 'Auvergne-Rhône-Alpes', '74': 'Auvergne-Rhône-Alpes',
    '21': 'Bourgogne-France-Comté', '25': 'Bourgogne-France-Comté', '39': 'Bourgogne-France-Comté', '58': 'Bourgogne-France-Comté',
    '70': 'Bourgogne-France-Comté', '71': 'Bourgogne-France-Comté', '89': 'Bourgogne-France-Comté', '90': 'Bourgogne-France-Comté',
    '22': 'Bretagne', '29': 'Bretagne', '35': 'Bretagne', '56': 'Bretagne',
    '18': 'Centre-Val de Loire', '28': 'Centre-Val de Loire', '36': 'Centre-Val de Loire', '37': 'Centre-Val de Loire',
    '41': 'Centre-Val de Loire', '45': 'Centre-Val de Loire',
    '08': 'Grand Est', '10': 'Grand Est', '51': 'Grand Est', '52': 'Grand Est', '54': 'Grand Est', '55': 'Grand Est',
    '57': 'Grand Est', '67': 'Grand Est', '68': 'Grand Est', '88': 'Grand Est',
    '02': 'Hauts-de-France', '59': 'Hauts-de-France', '60': 'Hauts-de-France', '62': 'Hauts-de-France', '80': 'Hauts-de-France',
    '75': 'Île-de-France', '77': 'Île-de-France', '78': 'Île-de-France', '91': 'Île-de-France', '92': 'Île-de-France',
    '93': 'Île-de-France', '94': 'Île-de-France', '95': 'Île-de-France',
    '14': 'Normandie', '27': 'Normandie', '50': 'Normandie', '61': 'Normandie', '76': 'Normandie',
    '16': 'Nouvelle-Aquitaine', '17': 'Nouvelle-Aquitaine', '19': 'Nouvelle-Aquitaine', '23': 'Nouvelle-Aquitaine', 
    '24': 'Nouvelle-Aquitaine', '33': 'Nouvelle-Aquitaine', '40': 'Nouvelle-Aquitaine', '47': 'Nouvelle-Aquitaine', 
    '64': 'Nouvelle-Aquitaine', '79': 'Nouvelle-Aquitaine', '86': 'Nouvelle-Aquitaine', '87': 'Nouvelle-Aquitaine',
    '09': 'Occitanie', '11': 'Occitanie', '12': 'Occitanie', '30': 'Occitanie', '31': 'Occitanie', '32': 'Occitanie',
    '34': 'Occitanie', '46': 'Occitanie', '48': 'Occitanie', '65': 'Occitanie', '66': 'Occitanie', '81': 'Occitanie',
    '82': 'Occitanie', '44': 'Pays de la Loire', '49': 'Pays de la Loire', '53': 'Pays de la Loire', '72': 'Pays de la Loire',
    '85': 'Pays de la Loire', '04': 'Provence-Alpes-Côte d\'Azur', '05': 'Provence-Alpes-Côte d\'Azur', '06': 'Provence-Alpes-Côte d\'Azur',
    '13': 'Provence-Alpes-Côte d\'Azur', '83': 'Provence-Alpes-Côte d\'Azur', '84': 'Provence-Alpes-Côte d\'Azur'
}

# 1. Bar Plot for Number of Rechargeable Vehicles Over Time using Plotly
st.subheader('1. Number of Rechargeable Vehicles Over Time')

# Grouping data by year and summing up the number of rechargeable vehicles
vehicles_over_time = data.groupby('year')['nb_vp_rechargeables_el'].sum().reset_index()

# Creating a bar chart with Plotly
fig = px.bar(vehicles_over_time, 
             x='year', 
             y='nb_vp_rechargeables_el', 
             color_discrete_sequence=['#8EA8C3'],
             labels={'nb_vp_rechargeables_el': 'Number of Rechargeable Vehicles', 'year': 'Year'})  



# Display the Plotly chart in Streamlit
st.plotly_chart(fig)

st.divider()



# 2. Pie Chart for Types of Vehicles (Plotly version)
st.subheader('2. Distribution of Vehicle Types')

# Summing up the number of electric and non-electric vehicles
electric_vehicles = data['nb_vp_rechargeables_el'].sum()
total_vehicles = data['nb_vp'].sum()

# Calculate non-electric vehicles
non_electric_vehicles = total_vehicles - electric_vehicles

# Creating a dictionary for the vehicle counts
vehicle_counts = {
    'Electric': electric_vehicles,
    'Non-Electric': non_electric_vehicles
}

# Creating a DataFrame for Plotly
vehicle_df = pd.DataFrame({
    'Vehicle Type': list(vehicle_counts.keys()),
    'Count': list(vehicle_counts.values())
})

custom_colors = ['#23395B', '#8EA8C3']

# Plotting the pie chart with Plotly
fig = px.pie(vehicle_df, values='Count', names='Vehicle Type', 
             color_discrete_sequence=custom_colors, hole=0.4)

# Show the plot in Streamlit
st.plotly_chart(fig)

st.divider()


# 3. Line Plot for Total Vehicles Over Time
st.subheader('3. Total Vehicles Over Time')

# Grouping data by date_arrete and summing up the total number of vehicles
total_vehicles_over_time = data.groupby('date_arrete')['nb_vp'].sum().reset_index()

# Use Plotly to create the line plot
fig = px.line(total_vehicles_over_time, 
              x='date_arrete', 
              y='nb_vp', 
              markers=True, 
              line_shape='linear',
              labels={'nb_vp': 'Total Vehicles', 'date_arrete': 'Date'},
              )

fig.update_traces(line_color='#23395B', marker_color='#406E8E')

# Display the Plotly chart in Streamlit
st.plotly_chart(fig)

st.divider()

# 4. Total Number of Vehicles per Region (Electric vs Non-Electric)
st.subheader('4. Total Number of Vehicles per Region (Electric vs Non-Electric)')
# Extract the department from the 'codgeo' column (first two digits)
data['department_code'] = data['codgeo'].astype(str).str[:2]

# Map department codes to regions
data['region'] = data['department_code'].map(dept_to_region)

# Aggregate data by region (sum the number of electric vehicles)
region_data = data.groupby('region').agg({
    'nb_vp_rechargeables_el': 'sum',
    'nb_vp': 'sum'
}).reset_index()

# Calculate non-electric vehicles
region_data['nb_vp_non_electric'] = region_data['nb_vp'] - region_data['nb_vp_rechargeables_el']

# Sort regions by total number of vehicles (nb_vp) in descending order
region_data = region_data.sort_values(by='nb_vp', ascending=False)

# Create a stacked bar chart with Plotly
fig = go.Figure()

# Add Non-Electric Vehicles trace
fig.add_trace(go.Bar(
    x=region_data['nb_vp'],
    y=region_data['region'],
    orientation='h',  # Horizontal bar
    name='Non-Electric Vehicles',
    marker=dict(color='#23395B', line=dict(width=0))  # Remove border around bars
))

# Add Electric Vehicles trace
fig.add_trace(go.Bar(
    x=region_data['nb_vp_rechargeables_el'],
    y=region_data['region'],
    orientation='h',  # Horizontal bar
    name='Electric Vehicles',
    marker=dict(color='#406E8E', line=dict(width=0))  # Remove border around bars
))

# Update the layout to remove the border around the legend
fig.update_layout(
    barmode='stack',
    xaxis_title='Number of Vehicles',
    yaxis_title='Region',
    legend_title='Vehicle Type',
    template='plotly_white',
    height=800,
    legend=dict(borderwidth=0),  # Remove the border around the legend
)

# Show the Plotly chart in Streamlit
st.plotly_chart(fig)

st.divider()

# 5. Ranking of Regions by Percentage of Electric Vehicles
st.subheader('5. Ranking of Regions by Percentage of Electric Vehicles')
# Extract the department from the 'codgeo' column (first two digits)
data['department_code'] = data['codgeo'].astype(str).str[:2]

# Map department codes to regions
data['region'] = data['department_code'].map(dept_to_region)

# Aggregate data by region (sum the number of electric vehicles and total vehicles)
region_data = data.groupby('region').agg({
    'nb_vp_rechargeables_el': 'sum',
    'nb_vp': 'sum'
}).reset_index()

# Calculate the percentage of electric vehicles for each region     
region_data['electric_vehicle_percentage'] = (region_data['nb_vp_rechargeables_el'] / region_data['nb_vp'])*100

# Sort regions by the percentage of electric vehicles in descending order
region_data = region_data.sort_values(by='electric_vehicle_percentage', ascending=False)

# Plot the ranking of regions by percentage of electric vehicles using Plotly
fig = px.bar(
    region_data,
    x='electric_vehicle_percentage',
    y='region',
    orientation='h',
    color='electric_vehicle_percentage',
    color_continuous_scale='Blues',
    labels={'electric_vehicle_percentage': 'Percentage of Electric Vehicles (%)', 'region': 'Region'},
    height=800
)

# Update the layout to display the x-axis as a percentage
fig.update_layout(
    xaxis_tickformat='.2f%',  # Set tick format to percentage with 2 decimal places
    xaxis_range=[0, 5],     # Set x-axis range to go from 0 to 100%
    xaxis_title='Percentage of Electric Vehicles (%)',
    yaxis_title='Region',
    coloraxis_colorbar=dict(title="Percentage of EVs (%)")
)

# Show the Plotly chart in Streamlit
st.plotly_chart(fig)