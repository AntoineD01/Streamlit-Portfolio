import streamlit as st
from st_social_media_links import SocialMediaIcons

st.title("Antoine Dupont")
st.write("**Data Scientist** | **AI Enthusiast** | **Engineer**")
st.write("Location: Paris, France")

# About Me
st.title("🤙 About Me")
st.write("""
    I am a Data Scientist with a background in engineering. I have worked on numerous projects involving data analysis, 
    predictive modeling, and machine learning. My passion lies in using data to solve complex problems and create 
    impactful solutions.
    """)


# Skills
st.title("🤹🏻 Skills Overview : ")

st.title('Programming Languages:')
st.write("**Python (and related libraries**")
st.progress(90)
st.write("**SQL**")
st.progress(70)
st.write("**PowerBI**")
st.progress(50)

st.title('Machine Learning:')
st.write("**Scikit-learn**")
st.progress(65)
st.write("**XGBoost**")
st.progress(35)

st.title('Other Tools:')
st.write("**Git**")
st.progress(70)
st.write("**Jupyter**")
st.progress(80)
st.write("**VSCode**")
st.progress(80)
st.write('**Excel**')
st.progress(75)

# Experience
st.title("🧑‍💼 Experience")
st.write("### Private tutor | Acadomia")
st.write("""
    - Adaptation to meet individual needs.
    - Strengthening listening skills to understand and address difficulties.
    - Planning sessions to achieve objectives.
    """)

st.write("### Multi-skilled employee | La Grande Récré")
st.write("""
    - Greet and advise customers.
    - Adapt to an intense environment.
    - Display products attractively.
    """)    

# Projects Section
st.title("⌨️ Projects")
st.write("### 1. Uber Data Analysis")
st.write("""
    In this project, I performed exploratory data analysis on Uber ride data to understand patterns in ride demand, fare trends, 
    and peak hours. The analysis was visualized using Streamlit and Folium.
    - **Technologies used:** Python, Pandas, Folium, Streamlit
    """)
st.write("### 2. Machine Learning Model for Patent Prediction")
st.write("""
    Developed a machine learning model to predict patent approval based on the text of applications. The model uses NLP to analyze content and forecast outcomes, helping assess patentability before submission.
    - **Technologies used:** Python, Scikit-learn, Pandas
    """)

# Education
st.header("🏫 Education")
st.write("### Master of Science in Data Engineering | Efrei Paris")
st.write("2021 - 2026")
st.progress(80)

# Contact Section
st.header("📇 Contact Me")
st.write("Feel free to reach out to me via email or LinkedIn. I'm always open to discussing new opportunities and collaborations!")
st.write("📧 **Email:** antoine.dupont@efrei.net")

# Footer
st.write("---")
social_media_links = [
    "https://linkedin.com/in/antoine-dupont0",
    "https://github.com/AntoineD01",
]

social_media_icons = SocialMediaIcons(social_media_links)
social_media_icons.render()
st.write("\n\n")
st.write("Created using [Streamlit](https://streamlit.io/) | © 2024 Antoine Dupont")