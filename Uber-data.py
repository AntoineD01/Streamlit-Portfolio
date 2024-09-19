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

# Initialize session state for button
if 'button' not in st.session_state:
    st.session_state.button = False

# Function to toggle the button state
def click_button():
    st.session_state.button = not st.session_state.button

# Create a button in the sidebar to toggle the data display
st.button("Toggle Pickup/Dropoff Data", on_click=click_button)

filtered_data_pickup = pd.DataFrame()
filtered_data_dropoff = pd.DataFrame()

# Use session state to determine which data to show
show_pickup = st.session_state.button
show_dropoff = not st.session_state.button

# Add a new column for tip/fare ratio
data2['tip/fare'] = data2['tip_amount'] / data2['fare_amount']

# Handle NaN values
data2['tip/fare'].replace(to_replace=0, value=np.nan, inplace=True)

data2['tpep_pickup_datetime'] = pd.to_datetime(data2['tpep_pickup_datetime'])
data2['tpep_dropoff_datetime'] = pd.to_datetime(data2['tpep_dropoff_datetime'])


if show_pickup:
    st.title("Uber Pickups in New York City (2014)")
    
    ### Visualization 1: Bar Chart of Pickups by Hour ###
    st.subheader(f"1. Pickups over time (All Data)")
    hourly_pickups_filtered = data2['tpep_pickup_datetime'].dt.hour.value_counts().sort_index()
    st.bar_chart(hourly_pickups_filtered, color = '#23395B')

    # Data per hour
    st.write("### Filter the data per hour ###")
    hour = st.slider("Select Hour to Filter Data", 0, 23)

    filtered_data1 = data2[data2['tpep_pickup_datetime'].dt.hour == hour]

    pickup_counts_by_minute = filtered_data1.set_index('tpep_pickup_datetime').resample('T').size()
    st.line_chart(pickup_counts_by_minute)


elif show_dropoff:
    st.title("Uber Dropoffs in New York City (2014)")
    
    ### Visualization 1: Bar Chart of Pickups by Hour ###
    st.subheader(f"1. Dropoffs over time (All Data)")
    hourly_dropoffs_filtered = data2['tpep_dropoff_datetime'].dt.hour.value_counts().sort_index()
    st.bar_chart(hourly_dropoffs_filtered, color='#CBF7ED')

    # Data per hour
    st.write("### Filter the data per hour ###")
    hour1 = st.slider("Select Hour to Filter Data", 0, 23)

    filtered_data2 = data2[data2['tpep_dropoff_datetime'].dt.hour == hour1]

    dropoff_counts_by_minute = filtered_data2.set_index('tpep_dropoff_datetime').resample('T').size()
    st.line_chart(dropoff_counts_by_minute)


st.divider()

