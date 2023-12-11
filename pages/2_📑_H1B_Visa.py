import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(r'Data/h1_grader_data.tsv', sep='\t')
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
st.set_page_config(layout="centered")
st.title("📑 H1B Sponsorship Information")

job_to_category = {v: k for k, v in category_to_job.items()}

# Let the user select a job title
selected_job = st.selectbox("What is your desired job title?", options=list(category_to_job.values()))

# Get the related category_code based on the selected job title
selected_category = job_to_category[selected_job]

# Filtering the dataframe based on chosen job title
filtered_df = df[df['category_code'] == selected_category]

# Get the top 10 sponsoring companies for the selected job title
top_companies = filtered_df.groupby('employer_name')['count'].sum().nlargest(10)

# Plotting the bar chart
st.subheader(f'Top 10 Sponsoring Companies for {selected_job}')
plt.figure(figsize=(10, 6))
plt.bar(top_companies.index, top_companies.values, color='#d0d49c')
plt.xticks(rotation=45, ha='right')
plt.xlabel('Company')
plt.ylabel('Visa Count')
st.pyplot(plt)