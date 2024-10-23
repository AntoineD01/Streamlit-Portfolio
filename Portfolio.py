import streamlit as st

homepage = st.Page('Homepage.py', title='Home', icon=':material/home:', default=True)

uber_data = st.Page("Uber-data.py", title="Uber Data", icon=":material/dashboard:",)

cars = st.Page("Cars.py", title="Cars", icon=":material/filter:",)

about_me = st.Page("About_me.py", title="About Me", icon=":material/person:",)



pg = st.navigation(
    {
        "Home": [homepage],
        "Projects": [uber_data, cars],
        "About me": [about_me],
    }   
)

pg.run()