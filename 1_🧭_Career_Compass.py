import streamlit as st

st.set_page_config(
    page_title = "Career Compass",
    page_icon= "🧭",
    layout="centered"
)
st.title("🧭 Career Compass")

st.sidebar.success("Select a page above")

st.header('🎯Vision', divider='violet')

multi = '''Empower job seekers by providing comprehensive data on job opportunities,
required skills, salary ranges, visa sponsorship, and location-specific hiring trends,
allowing users to make informed career decisions.
'''
st.markdown(multi)

st.header('🤓Team', divider='violet')


col1, col2, col3, col4 = st.columns(4)

with col1:
      st.image('Images/Pragyan.jpg', caption='Pragyan Aryal')

with col2:
      st.image('Images/Ankita.png', caption='Ankita Bodigam')

with col3:
      st.image('Images/Amogh.jpg', caption='Amogh Borikar')

with col4:
      st.image('Images/Prakhar.png', caption='Prakhar Sharma')

st.divider()

col5, col6 = st.columns([3, 1])

with col5:
      st.subheader("Course: Data Focused Python")
      st.image('Images/CMU.png', width=200)

with col6:
      st.subheader("Data used:")
      st.link_button("Indeed", "https://www.indeed.com/")
      st.link_button("USA Jobs", "https://www.usajobs.gov/")
      st.link_button("Geo Locations", "https://positionstack.com/")
      st.link_button("H1B Data", "https://h1bgrader.com/")