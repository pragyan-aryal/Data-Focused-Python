import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_parquet('Data//Indeed/Indeed_Data.parquet')
df = df.loc[df['country_code'] == 'USA']

category_to_job = {
    'SE': "Software Engineer",
    'DA': "Data Analyst",
    'PM': "Product Manager",
    'PJM': "Project Manager",
    'BA': "Business Analyst",
    'DE': "Data Engineer",
    'ME': "Mechanical Engineer",
    'CAE': "CAE Engineer",
    'FEA': "FEA Engineer",
    'CE': "Civil Engineer"
}

st.title("Map")

job_to_category = {v: k for k, v in category_to_job.items()}

# Let the user select a job title
selected_job = st.selectbox("What is your desired job title?", options=list(category_to_job.values()))

# Get the related category_code based on the selected job title
selected_category = job_to_category[selected_job]

# Filtering the dataframe based on chosen job title
filtered_df = df[df['Category'] == selected_category]

fig = px.density_mapbox(filtered_df, lat = 'latitude', lon = 'longitude',
                        radius = 8,
                        zoom = 2.5,
                        color_continuous_scale=["blue", "green", "yellow", "red"],
                        mapbox_style = 'open-street-map')
st.plotly_chart(fig)
