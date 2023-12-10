import streamlit as st

st.set_page_config(
    page_title = "Career Compass",
    page_icon= "🧭",
)

st.title("Career Compass")

st.sidebar.success("Select a page above")

st.header('🎯Vision', divider='black')

multi = '''Empower job seekers by providing comprehensive data on job opportunities,
required skills, salary ranges, visa sponsorship, and location-specific hiring trends,
allowing users to make informed career decisions.
'''
st.markdown(multi)