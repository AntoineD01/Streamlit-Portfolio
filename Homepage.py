import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer
from huggingface_hub import login

st.title("🏠 Home")
st.write("Welcome to My Portfolio!")
st.write("Hello! I'm Antoine Dupont, a data scientist with a passion for AI, machine learning, and data visualization. "
         "I have experience in developing data-driven solutions and enjoy working on projects that turn data into insights.")

st.title("🚧 Work in Progress")


#Ideas :
#Quizz
st.header("Test Your Knowledge About Me!")
question = st.radio(
    "Which programming language do I use the most?",
    ('Python', 'Java', 'R'))

if question == 'Python':
    st.success("Correct! Python is my go-to language.")
else:
    st.error("Nope, it's Python.")

#Fun Fact
import random

st.header("Learn Something Fun About Me!")
if st.button("Generate Fun Fact"):
    fun_facts = [
        "I’m a huge fan of chess and often play online.",
        "I love hiking and exploring nature trails.",
        "I’ve worked on over 10 different data science projects."
    ]
    st.write(random.choice(fun_facts))