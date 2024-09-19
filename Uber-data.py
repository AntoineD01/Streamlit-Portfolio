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

show_pickup = st.checkbox("Show Pickup Data", value=True)
show_dropoff = st.checkbox("Show Dropoff Data", value=False)

filtered_data_pickup = pd.DataFrame()
filtered_data_dropoff = pd.DataFrame()

if show_pickup:
    filtered_data_pickup = data2[['tpep_pickup_datetime', 'pickup_latitude', 'pickup_longitude']]

if show_dropoff:
    filtered_data_dropoff = data2[['tpep_pickup_datetime', 'dropoff_latitude', 'dropoff_longitude']]

# Add a new column for tip/fare ratio
data2['tip/fare'] = data2['tip_amount'] / data2['fare_amount']

# Handle NaN values
data2['tip/fare'].replace(to_replace=0, value=np.nan, inplace=True)

data2['tpep_pickup_datetime'] = pd.to_datetime(data2['tpep_pickup_datetime'])
data2['tpep_dropoff_datetime'] = pd.to_datetime(data2['tpep_dropoff_datetime'])



if show_pickup and show_dropoff:
    st.write("### Showing both Pickup and Dropoff Data")
    filtered_data_pickup.columns = ['tpep_pickup_datetime', 'latitude', 'longitude']
    filtered_data_dropoff.columns = ['tpep_pickup_datetime', 'latitude', 'longitude']
    filtered_data = pd.concat([filtered_data_pickup, filtered_data_dropoff])
elif show_pickup:
    st.title("Uber Pickups in New York City (2014)")
    filtered_data = filtered_data_pickup.rename(columns={'pickup_latitude': 'latitude', 'pickup_longitude': 'longitude'})

    ### Visualization 1: Bar Chart of Pickups by Hour ###
    st.subheader(f"1. Pickups over time (All Data)")
    hourly_pickups_filtered = data2['tpep_pickup_datetime'].dt.hour.value_counts().sort_index()
    st.bar_chart(hourly_pickups_filtered, color = '#23395B')


elif show_dropoff:
    st.title("Uber Dropoffs in New York City (2014)")
    filtered_data = filtered_data_dropoff.rename(columns={'dropoff_latitude': 'latitude', 'dropoff_longitude': 'longitude'})

    ### Visualization 1: Bar Chart of Pickups by Hour ###
    st.subheader(f"1. Pickups over time (All Data)")
    hourly_dropoffs_filtered = data2['tpep_dropoff_datetime'].dt.hour.value_counts().sort_index()
    st.bar_chart(hourly_dropoffs_filtered, color='#CBF7ED')



# Data per hour
st.write("### Filter the data per hour ###")
hour = st.slider("Select Hour to Filter Data", 0, 23)

filtered_data = data2[data2['tpep_pickup_datetime'].dt.hour == hour]

### Visualization 1: Line Chart of Pickups over Time ###
# Resample data by minute and count pickups
pickup_counts_by_minute = filtered_data.set_index('tpep_pickup_datetime').resample('T').size()
st.line_chart(pickup_counts_by_minute)


