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
st.set_page_config(layout="wide")
st.title("🗺️ Job Locations")

job_to_category = {v: k for k, v in category_to_job.items()}

col1, col2 = st.columns(2)

with col1:
      selected_job = st.selectbox("What is your desired job title?", options=list(category_to_job.values()))

with col2:
      plot_type = st.selectbox("Select plot type", ["Scatterplot", "Heatmap"])

# Get the related category_code based on the selected job title
selected_category = job_to_category[selected_job]

# Filtering the dataframe based on chosen job title
filtered_df = df[df['Category'] == selected_category]

if plot_type == "Scatterplot":
    fig = px.scatter_mapbox(filtered_df, lat="latitude", lon="longitude",
                            color="Category",
                            zoom = 2.5,
                            color_continuous_scale=["red", "darkred"],
                            mapbox_style = 'open-street-map')
    fig.update_traces(marker=dict(color='red', size=10))

else:
    fig = px.density_mapbox(filtered_df, lat = 'latitude', lon = 'longitude',
                        radius = 8,
                        zoom = 2.5,
                        color_continuous_scale=["blue", "green", "yellow", "red"],
                        mapbox_style = 'open-street-map')

fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=600, width=1400, mapbox_style="open-street-map")
st.plotly_chart(fig)
