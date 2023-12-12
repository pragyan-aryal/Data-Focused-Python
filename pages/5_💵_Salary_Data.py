import streamlit as st
import pandas as pd
import plotly.express as px
import re

# Input File
df = pd.read_parquet('Final_Data/Final/merged.parquet')

# salary bins
salary_bins = [0, 75000, 100000, 125000, float('inf')]
salary_labels = ['<75000', '75000-100000', '100000-125000', '125000 and above']

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

categories_in_data = df['Category'].unique()

relevant_jobs = {k: v for k, v in category_to_job.items() if k in categories_in_data}

st.set_page_config(layout="centered")
st.title('💵 Salary Distribution')

col1, col2 = st.columns(2)

with col1:
      selected_category = st.selectbox('Select Category', relevant_jobs.values())

with col2:
      selected_experience_level = st.selectbox('Select Experience Level', df['Experience_Level'].unique())

category = ""

for key, value in category_to_job.items():
    if value == selected_category:
        category = key
        break


selected_data = df.loc[(df['Category'] == category) & (df['Experience_Level'] == selected_experience_level)]

selected_data['Salary_Bin'] = pd.cut(selected_data['MaxSalary'], bins=salary_bins, labels=salary_labels, right=False)

salary_counts = selected_data['Salary_Bin'].value_counts().sort_index()

fig = px.pie(salary_counts, names=salary_counts.index, values=salary_counts.values,
             labels={'label': 'Salary Range', 'value': 'Count'})

st.plotly_chart(fig)