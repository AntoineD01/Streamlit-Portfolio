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

# Add a new column for tip/fare ratio
data2['tip/fare'] = data2['tip_amount'] / data2['fare_amount']

# Handle NaN values
data2['tip/fare'].replace(to_replace=0, value=np.nan, inplace=True)

data2['tpep_pickup_datetime'] = pd.to_datetime(data2['tpep_pickup_datetime'])
data2['tpep_dropoff_datetime'] = pd.to_datetime(data2['tpep_dropoff_datetime'])

st.title("Uber Pickups in New York City (2014)")


### Visualization 2: Bar Chart of Pickups by Hour ###
st.subheader(f"1. Pickups over time (All Data)")
hourly_pickups_filtered = data2['tpep_pickup_datetime'].dt.hour.value_counts().sort_index()
st.bar_chart(hourly_pickups_filtered)

# Data per hour
st.write("### Filter the data per hour ###")
hour = st.slider("Select Hour to Filter Data", 0, 23)

filtered_data = data2[data2['tpep_pickup_datetime'].dt.hour == hour]

### Visualization 1: Line Chart of Pickups over Time ###
# Resample data by minute and count pickups
pickup_counts_by_minute = filtered_data.set_index('tpep_pickup_datetime').resample('T').size()
st.line_chart(pickup_counts_by_minute)


### Visualization 2: Map of Uber Pickups ###
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