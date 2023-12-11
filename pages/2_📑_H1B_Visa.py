import streamlit as st
import pandas as pd
import plotly.express as px

# Input File
df = pd.read_csv('Final_Data/Final/h1_grader_data.tsv', sep='\t')
df = df.drop('category_code.1', axis=1)

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
st.title("📑 H1B Sponsorship Information")

job_to_category = {v: k for k, v in category_to_job.items()}

categories_in_data = df['category_code'].unique()
jobs_in_data = [category_to_job[x] for x in categories_in_data]

col1, col2, col3 = st.columns(3)

with col2:
    selected_job = st.selectbox("What is your desired job title?", options=jobs_in_data)

selected_category = job_to_category[selected_job]

filtered_df = df[df['category_code'] == selected_category]

top_companies = filtered_df.groupby('employer_name')['count'].sum().nlargest(10)

st.subheader(f'Top 10 Sponsoring Companies for {selected_job} Position')
fig = px.bar(top_companies, x=top_companies.index, y=top_companies.values, 
             labels={'x':'Company', 'y':'Visa Count'}, width=1400, height=800)
fig.update_layout(xaxis_tickangle=45)

st.plotly_chart(fig)