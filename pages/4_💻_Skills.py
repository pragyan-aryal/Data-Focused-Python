import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(r'Data/Indeed/all_skills.tsv', sep='\t')

df.columns = ['Skill', 'job_id', 'category_code', 'job_level', 'skill_type']

cat1_filter = st.selectbox('Category 1', df['category_code'].unique())
cat2_filter = st.selectbox('Category 2', df['job_level'].unique()) 
cat3_filter = st.selectbox('Category 3', df['skill_type'].unique())

filtered_df = df[(df['category_code'] == cat1_filter) & 
                 (df['job_level'] == cat2_filter) &
                 (df['skill_type'] == cat3_filter)]

skills = filtered_df['Skill'].value_counts().nlargest(10)

st.bar_chart(skills)

