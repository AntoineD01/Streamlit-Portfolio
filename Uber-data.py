#https://www.data.gouv.fr/fr/datasets/voitures-particulieres-immatriculees-par-commune-et-par-type-de-recharge-jeu-de-donnees-aaadata/

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pydeck as pdk

# Load Data
@st.cache_data
def load_data():
    path2 = "https://raw.githubusercontent.com/uber-web/kepler.gl-data/master/nyctrips/data.csv"
    data2 = pd.read_csv(path2, delimiter=',')
    return data2

data2 = load_data()

# Title
st.title("🚗 Uber Data Analysis")
# Display Data
st.write("### Uber NYC Trips Data (April 2014)")
st.write("Here is the head of the data we are currently using for analysis.")
st.dataframe(data2.head())

# Data Description
st.write("### Data Description")
st.dataframe(data2.describe())

# Add a new column for tip/fare ratio
data2['tip/fare'] = data2['tip_amount'] / data2['fare_amount']

# Handle NaN values
data2['tip/fare'].replace(to_replace=0, value=np.nan, inplace=True)

data2['tpep_pickup_datetime'] = pd.to_datetime(data2['tpep_pickup_datetime'])
data2['tpep_dropoff_datetime'] = pd.to_datetime(data2['tpep_dropoff_datetime'])

# Scatter plot for pickup locations
st.write("### Scatter Plot - Pickup Locations")
fig1, ax1 = plt.subplots(figsize=(10, 10), dpi=100)
ax1.set_title('Scatter plot - Uber - April 2014 (Pickups)')
ax1.set_xlabel('Latitude')
ax1.set_ylabel('Longitude')
ax1.scatter(data2['pickup_latitude'], data2['pickup_longitude'], s=0.8, alpha=0.4, color='#23395B')
ax1.set_ylim(-74.05, -73.85)
ax1.set_xlim(40.65, 40.85)
st.pyplot(fig1)

# Scatter plot for dropoff locations
st.write("### Scatter Plot - Dropoff Locations")
fig2, ax2 = plt.subplots(figsize=(10, 10), dpi=100)
ax2.set_title('Scatter plot - Uber - April 2014 (Dropoffs)')
ax2.set_xlabel('Latitude')
ax2.set_ylabel('Longitude')
ax2.scatter(data2['dropoff_latitude'], data2['dropoff_longitude'], s=0.8, alpha=0.4, color='#406E8E')
ax2.set_ylim(-74.05, -73.85)
ax2.set_xlim(40.65, 40.85)
st.pyplot(fig2)

st.title("Uber Pickups in New York City (2014)")

# Add a slider for selecting an hour
hour = st.slider("Select Hour to Filter Data", 0, 23)

# Filter data based on selected hour
filtered_data = data2[data2['tpep_pickup_datetime'].dt.hour == hour]

### Visualization 1: Line Chart of Pickups over Time ###
st.subheader(f"1. Pickups over Time (Filtered for {hour}:00)")
pickup_counts_filtered = filtered_data.set_index('tpep_pickup_datetime').resample('H').size()
st.line_chart(pickup_counts_filtered)

### Visualization 2: Bar Chart of Pickups by Hour ###
st.subheader(f"2. Pickups by Hour (Filtered for {hour}:00)")
hourly_pickups_filtered = filtered_data['tpep_pickup_datetime'].dt.hour.value_counts().sort_index()
st.bar_chart(hourly_pickups_filtered)

### Visualization 3: Map of Uber Pickups ###
st.subheader("3. Geographic Distribution of Uber Pickups (Map)")

# Use pydeck for interactive map visualization
st.map(filtered_data[['Lat', 'Lon']].dropna())

# Advanced Map using pydeck
st.subheader("Advanced Pickup Map")
map_layer = pdk.Layer(
    "HexagonLayer",
    data=filtered_data[['Lat', 'Lon']],
    get_position='[Lon, Lat]',
    radius=100,
    elevation_scale=4,
    elevation_range=[0, 1000],
    pickable=True,
    extruded=True,
)

# Set the map view
view_state = pdk.ViewState(
    longitude=-74.00, latitude=40.71, zoom=10, pitch=50,
)

# Render the map
map_view = pdk.Deck(layers=[map_layer], initial_view_state=view_state)
st.pydeck_chart(map_view)

### Visualization 4: Heatmap of Pickup Density ###
st.subheader("4. Heatmap of Uber Pickup Density")

# Create a heatmap using Seaborn
fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(data=filtered_data, x="Lon", y="Lat", bins=30, pthresh=.1, cmap="coolwarm", ax=ax)
plt.title("Heatmap of Uber Pickups")
st.pyplot(fig)

### Visualization 5: Histogram of Pickups per Day ###
st.subheader("5. Histogram of Pickups per Day")

# Group by day and plot the distribution
data2['day'] = data2['tpep_tpep_pickup_datetime'].dt.day
fig, ax = plt.subplots()
sns.histplot(data2['day'], kde=False, ax=ax)
ax.set_title("Pickups per Day")
st.pyplot(fig)