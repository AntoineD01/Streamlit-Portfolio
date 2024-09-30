import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
import plotly.graph_objects as go


# Load Data
@st.cache_data
def load_data():
    path2 = "https://raw.githubusercontent.com/uber-web/kepler.gl-data/master/nyctrips/data.csv"
    data2 = pd.read_csv(path2, delimiter=',')
    return data2

data2 = load_data()

# Title
st.title("🚗 Uber Data Analysis")

#Cleaning the data
data2['tpep_pickup_datetime'] = pd.to_datetime(data2['tpep_pickup_datetime'])
data2['tpep_dropoff_datetime'] = pd.to_datetime(data2['tpep_dropoff_datetime'])

data2 = data2[(data2['fare_amount'] > 0) & (data2['trip_distance'] > 0)]

# Filter out invalid longitude values in pickup locations
data2 = data2[
    (data2['pickup_longitude'] >= -74.2) & 
    (data2['pickup_longitude'] <= -73.9)
]

# The button feature
if 'button' not in st.session_state:
    st.session_state.button = False

def click_button():
    st.session_state.button = not st.session_state.button

st.button("Toggle Pickup/Dropoff Data", on_click=click_button)

filtered_data_pickup = pd.DataFrame()
filtered_data_dropoff = pd.DataFrame()

show_pickup = st.session_state.button
show_dropoff = not st.session_state.button

#Comparison between pickup and dropoff

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

    pickup_counts_by_minute = filtered_data1.set_index('tpep_pickup_datetime').resample('min').size()
    st.line_chart(pickup_counts_by_minute, color = '#23395B')

    # Rename columns for pickup locations
    pickup_locations = data2[['pickup_latitude', 'pickup_longitude']].rename(columns={
    'pickup_latitude': 'lat',
    'pickup_longitude': 'lon'
    })

    st.write("### Pickup Locations in NYC")
    st.map(pickup_locations, color = '#23395B')


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

    dropoff_counts_by_minute = filtered_data2.set_index('tpep_dropoff_datetime').resample('min').size()
    st.line_chart(dropoff_counts_by_minute, color='#CBF7ED')

    # Rename columns for dropoff locations
    dropoff_locations = data2[['dropoff_latitude', 'dropoff_longitude']].rename(columns={
    'dropoff_latitude': 'lat',
    'dropoff_longitude': 'lon'
    })

    st.write("### Dropoff Locations in NYC")
    st.map(dropoff_locations, zoom=9, color='#CBF7ED')


st.divider()

st.write("### Trip Distance Distribution")

# Histogram of trip distances
fig, ax = plt.subplots(figsize=(8, 6))
fig.patch.set_facecolor('#0f1116')
ax.hist(data2['trip_distance'], bins=50, color='#93c7fa', alpha=0.7)
ax.set_facecolor('#0f1116')  # Background color inside the plot
ax.set_xlim(0, 20)
ax.set_xlabel('Trip Distance (miles)', color='#ffffff', fontsize=12)
ax.set_ylabel('Number of Trips', color='#ffffff', fontsize=12)
ax.tick_params(axis='x', colors='#ffffff')  # X-axis ticks
ax.tick_params(axis='y', colors='#ffffff')  # Y-axis ticks
ax.spines['bottom'].set_color('#ffffff')  # X-axis color
ax.spines['left'].set_color('#ffffff')  # Y-axis color
ax.spines['top'].set_visible(False)  # Turn off top spine
ax.spines['right'].set_visible(False)  # Turn off right spine

st.pyplot(plt)


st.divider()

st.write("### Total Revenue Over Time")

# Create a new column for total revenue
data2['total_revenue'] = data2['fare_amount'] + data2['tip_amount']

# Resample data by hour and calculate total revenue per hour
total_revenue_per_hour = data2.resample('h', on='tpep_pickup_datetime')['total_revenue'].sum()

# Plot line chart of revenue over time
st.line_chart(total_revenue_per_hour)

st.divider()

st.write("### Average Speed of Trips Over Time")

# Calculate speed (distance / time in hours)
data2['trip_time_hours'] = (data2['tpep_dropoff_datetime'] - data2['tpep_pickup_datetime']).dt.total_seconds() / 3600
data2.loc[data2['trip_time_hours'] == 0, 'trip_time_hours'] = np.nan


data2['speed_mph'] = data2['trip_distance'] / data2['trip_time_hours']

# Resample to hourly average speed
avg_speed_per_hour = data2.resample('h', on='tpep_pickup_datetime')['speed_mph'].mean()

# Plot line chart of average speed over time
st.line_chart(avg_speed_per_hour)

st.divider()

X = data2[['trip_distance']]  # Features (distance)
y = data2['fare_amount']  # Target (fare amount)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict on the test set
y_pred = model.predict(X_test)

# Model evaluation: Calculate MAE and R-squared
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# Display model performance
st.write(f"### Machine Learning Model Predicting Fare Amount")
st.write(f"The margin of error (MAE) is around : ${mae:.2f}")

# Allow the user to input a distance to predict the fare
st.write("### Predict the Fare Based on Distance")
distance_input = st.number_input("Enter the trip distance in miles:", min_value=0.0, step=0.1)

if distance_input > 0:
    predicted_fare = model.predict(np.array([[distance_input]]))[0]
    st.write(f"Predicted fare for a distance of {distance_input} miles: ${predicted_fare:.2f}")
