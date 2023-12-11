import streamlit as st
import pandas as pd
import plotly.express as px
import re  # Import the 're' module for regular expressions

# Read a Parquet file
df = pd.read_parquet(r'Data/Indeed/Indeed_Data.parquet')
# Now 'df' is a DataFrame containing the data from the Parquet file

# Define salary bins
salary_bins = [0, 75000, 100000, 125000, float('inf')]
salary_labels = ['<75000', '75000-100000', '100000-125000', '125000 and above']

# Streamlit app
st.title('💵 Salary Distribution Dashboard')

col1, col2 = st.columns(2)

with col1:
      selected_category = st.selectbox('Select Category', df['Category'].unique())

with col2:
      selected_experience_level = st.selectbox('Select Experience Level', df['Experience_Level'].unique())

# Filter data based on selected category and experience level
selected_data = df[(df['Category'] == selected_category) & (df['Experience_Level'] == selected_experience_level)]

# Create salary bins and count the occurrences in each bin
selected_data['Salary_Bin'] = pd.cut(selected_data['MaxSalary'], bins=salary_bins, labels=salary_labels, right=False)
salary_counts = selected_data['Salary_Bin'].value_counts().sort_index()

# Create donut chart using Plotly Express
fig = px.pie(salary_counts, names=salary_counts.index, values=salary_counts.values,
             hole=0.3, title=f'Salary Distribution for {selected_category} ({selected_experience_level} Level)',
             labels={'label': 'Salary Range', 'value': 'Count'})

# Show the figure using Streamlit
st.plotly_chart(fig)