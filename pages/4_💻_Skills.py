import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("💻 Top Skills Appearing in job descriptions")
import matplotlib.pyplot as plt

df = pd.read_csv(r'Data/Indeed/all_skills.tsv', sep='\t')

df.columns = ['Skill', 'job_id', 'category_code', 'job_level', 'skill_type']

col1, col2, col3 = st.columns(3)

with col1:
      cat1_filter = st.selectbox('Select your desired job title:', df['category_code'].unique())

with col2:
      cat2_filter = st.selectbox('Select level of job:', df['job_level'].unique()) 

with col3:
      cat3_filter = st.selectbox('Select Skill type: ', df['skill_type'].unique())

filtered_df = df[(df['category_code'] == cat1_filter) & 
                 (df['job_level'] == cat2_filter) &
                 (df['skill_type'] == cat3_filter)]

skills = filtered_df['Skill'].value_counts().nlargest(10)

fig = px.bar(skills, x=skills.index, y=skills.values, width=1400, height=600)

fig.update_layout(
    title='Top Skills',
    xaxis_title=f'{cat3_filter}', 
    yaxis_title='Number of Occurrences in Job Descriptions'
)
st.write(fig)

from wordcloud import WordCloud
text = " ".join(skills.index) 
wc = WordCloud(width=1400, height=600).generate(text)
st.image(wc.to_array())

