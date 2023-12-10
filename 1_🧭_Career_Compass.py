import streamlit as st

st.set_page_config(
    page_title = "Career Compass",
    page_icon= "🧭",
)

st.title("Career Compass")

st.sidebar.success("Select a page above")

st.header('🎯Vision', divider='rainbow')

multi = '''Empower job seekers by providing comprehensive data on job opportunities,
required skills, salary ranges, visa sponsorship, and location-specific hiring trends,
allowing users to make informed career decisions.
'''
st.markdown(multi)

st.header('🤓Team', divider='rainbow')


col1, col2, col3, col4 = st.columns(4)

with col1:
      st.image('Images/Pragyan.jpg', caption='Pragyan Aryal')

with col2:
      st.image('Images/Ankita.png', caption='Ankita Bodigam')

with col3:
      st.image('Images/Amogh.jpg', caption='Amogh Borikar')

with col4:
      st.image('Images/Prakhar.png', caption='Prakhar Sharma')