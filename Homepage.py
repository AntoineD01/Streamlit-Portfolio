import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer
from huggingface_hub import login

st.title("🏠 Home")
st.write("Welcome to My Portfolio!")
st.write("Hello! I'm Antoine Dupont, a data scientist with a passion for AI, machine learning, and data visualization. "
         "I have experience in developing data-driven solutions and enjoy working on projects that turn data into insights.")

st.title("🚧 Work in Progress")