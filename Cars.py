import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from geopy.geocoders import Nominatim
import time

@st.cache_data
def load_data():
    data = pd.read_csv('cars.csv', delimiter=',')  
    data.columns = data.columns.str.strip()  # Strip whitespace from column names
    return data
    
data = load_data()

st.title('Electric Vehicle Dataset')
st.write('This dataset contains information about electric vehicles.')

#Cleaning the data
st.write(data.head())
#We convert codgeo to int
data['codgeo'] = data['codgeo'].astype(str)

data = data[~data['codgeo'].str.startswith('2A')]
data = data[~data['codgeo'].str.startswith('2B')]

data['codgeo'] = data['codgeo'].astype(int)

data['date_arrete'] = pd.to_datetime(data['date_arrete'])
