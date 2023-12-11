import streamlit as st
import pandas as pd
import plotly.express as px

# Input File
df = pd.read_parquet('Final_Data/Final/merged.parquet')
df = df.loc[df['country_code'] == 'USA']

job_categories = df['Category'].unique()
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
job_to_category = {v: k for k, v in category_to_job.items()}

job_options = [category_to_job[c] for c in job_categories if c in category_to_job]

st.set_page_config(layout="wide")
st.title("🗺️ Job Locations")


col1, col2 = st.columns(2)

with col1:
      selected_job = st.selectbox( "What is your desired job title?", options=job_options)

with col2:
      plot_type = st.selectbox("Select plot type", ["Heatmap","Scatterplot"])

selected_category = job_to_category[selected_job]

filtered_df = df[df['Category'] == selected_category]

if plot_type == "Scatterplot":
    fig = px.scatter_mapbox(filtered_df, lat="latitude", lon="longitude",
                            color="Category",
                            zoom = 2.5,
                            color_continuous_scale=["red", "darkred"],
                            mapbox_style = 'open-street-map')
    fig.update_traces(marker=dict(color='red', size=10))
    fig.update_layout(showlegend=False)

else:
    fig = px.density_mapbox(filtered_df, lat = 'latitude', lon = 'longitude',
                        radius = 8,
                        zoom = 2.5,
                        color_continuous_scale=["blue", "green", "yellow", "red"],
                        mapbox_style = 'open-street-map')

fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=600, width=1400, mapbox_style="open-street-map")
st.plotly_chart(fig)
