#https://www.data.gouv.fr/fr/datasets/voitures-particulieres-immatriculees-par-commune-et-par-type-de-recharge-jeu-de-donnees-aaadata/


import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load Data
@st.cache_data
def load_data():
    path2 = "https://raw.githubusercontent.com/uber-web/kepler.gl-data/master/nyctrips/data.csv"
    data2 = pd.read_csv(path2, delimiter=',')
    return data2

data2 = load_data()

# Display Data
st.write("### Uber NYC Trips Data (April 2014)")
st.dataframe(data2.head())

# Data Description
st.write("### Data Description")
st.dataframe(data2.describe())

# Add a new column for tip/fare ratio
data2['tip/fare'] = data2['tip_amount'] / data2['fare_amount']
st.write("### Data with tip/fare column")
st.dataframe(data2.head())

# Handle NaN values
data2['tip/fare'].replace(to_replace=0, value=np.nan, inplace=True)

# Scatter plot for pickup locations
st.write("### Scatter Plot - Pickup Locations")
fig1, ax1 = plt.subplots(figsize=(10, 10), dpi=100)
ax1.set_title('Scatter plot - Uber - April 2014 (Pickups)')
ax1.set_xlabel('Latitude')
ax1.set_ylabel('Longitude')
ax1.scatter(data2['pickup_latitude'], data2['pickup_longitude'], s=0.8, alpha=0.4)
ax1.set_ylim(-74.1, -73.9)
ax1.set_xlim(40.7, 40.9)
st.pyplot(fig1)

# Scatter plot for dropoff locations
st.write("### Scatter Plot - Dropoff Locations")
fig2, ax2 = plt.subplots(figsize=(10, 10), dpi=100)
ax2.set_title('Scatter plot - Uber - April 2014 (Dropoffs)')
ax2.set_xlabel('Latitude')
ax2.set_ylabel('Longitude')
ax2.scatter(data2['dropoff_latitude'], data2['dropoff_longitude'], s=0.8, alpha=0.4)
ax2.set_ylim(-74.1, -73.9)
ax2.set_xlim(40.7, 40.9)
st.pyplot(fig2)
