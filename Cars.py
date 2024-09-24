import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium


@st.cache_data
def load_data():
    data = pd.read_csv('cars.csv', delimiter=',')  
    data.columns = data.columns.str.strip()  # Strip whitespace from column names
    return data
    
data = load_data()

st.title('Electric Vehicle Dataset')
st.write('This dataset contains information about electric vehicles.')

#Cleaning the data
#We convert codgeo to int and delete corsica
data['codgeo'] = data['codgeo'].astype(str)

data = data[~data['codgeo'].str.startswith('2A')]
data = data[~data['codgeo'].str.startswith('2B')]

data['codgeo'] = data['codgeo'].astype(int)

#We convert date_arrete to datetime
data['date_arrete'] = pd.to_datetime(data['date_arrete'])

# 1. Bar Plot for Number of Rechargeable Vehicles Over Time
st.subheader('1. Number of Rechargeable Vehicles Over Time')

# Grouping data by date_arrete and summing up the number of rechargeable vehicles
vehicles_over_time = data.groupby('date_arrete')['nb_vp_rechargeables_el'].sum().reset_index()

# Plotting
plt.figure(figsize=(12, 6))
sns.barplot(x='date_arrete', y='nb_vp_rechargeables_el', data=vehicles_over_time)
plt.xticks(rotation=45)
plt.title('Number of Rechargeable Vehicles Over Time')
plt.xlabel('Date of the decree')
plt.ylabel('Number of Rechargeable Vehicles')
plt.tight_layout()
st.pyplot(plt)


# 2. Pie Chart for Types of Vehicles
st.subheader('2. Distribution of Vehicle Types')

# Summing up the number of each type of vehicle
vehicle_counts = {
    'Electric': data['nb_vp_rechargeables_el'].sum(),
    'Gas': data['nb_vp_rechargeables_gaz'].sum(),
    'Total': data['nb_vp'].sum()
}

# Plotting
plt.figure(figsize=(8, 8))
plt.pie(vehicle_counts.values(), labels=vehicle_counts.keys(), autopct='%1.1f%%', startangle=140)
plt.title('Distribution of Vehicle Types')
plt.axis('equal')  # Equal aspect ratio ensures that pie chart is circular
st.pyplot(plt)

# 3. Scatter Plot of Latitude vs Longitude
st.subheader('Geographical Distribution of Rechargeable Vehicles')

plt.figure(figsize=(12, 6))
sns.scatterplot(data=data, x='longitude', y='latitude', size='nb_vp_rechargeables_el', sizes=(20, 200), legend=False)
plt.title('Geographical Distribution of Rechargeable Vehicles')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.grid()
st.pyplot(plt)

# 4. Line Plot for Total Vehicles Over Time
st.subheader('Total Vehicles Over Time')

# Grouping data by date_arrete and summing up the total number of vehicles
total_vehicles_over_time = data.groupby('date_arrete')['nb_vp'].sum().reset_index()

# Plotting
plt.figure(figsize=(12, 6))
sns.lineplot(x='date_arrete', y='nb_vp', data=total_vehicles_over_time, marker='o')
plt.xticks(rotation=45)
plt.title('Total Vehicles Over Time')
plt.xlabel('Date')
plt.ylabel('Total Vehicles')
plt.grid()
st.pyplot(plt)