import streamlit as st
import pandas as pd
import numpy as np


@st.cache_data
def load_data():
    try:
        # Use on_bad_lines to handle bad lines in the CSV
        data = pd.read_csv('cars.csv', delimiter=';', on_bad_lines='warn')
        return data
    except Exception as e:
        st.error(f"An error occurred while loading the data: {e}")
        return pd.DataFrame()

data1 = load_data()

st.title('Cars Dataset')
st.write('This dataset contains information about cars.')
st.dataframe(data1.describe())