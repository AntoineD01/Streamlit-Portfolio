import streamlit as st


homepage = st.Page('Homepage.py', title='Home', icon=':material/home:', default=True)

uber_data = st.Page("uber-data.py", title="Uber Data", icon=":material/dashboard:",)

about_me = st.Page("about_me.py", title="About Me", icon=":material/person:",)

pg = st.navigation(
    {
        "Home": [homepage],
        "Projects": [uber_data],
        "About_me": [about_me],
    }
)

pg.run()