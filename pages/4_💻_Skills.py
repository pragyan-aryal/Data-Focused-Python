import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("💻 Top Skills Appearing in job descriptions")

# Input File
df = pd.read_csv('Final_Data/Final/all_skills.tsv', sep='\t')
df.columns = ['Skill', 'job_id', 'category_code', 'job_level', 'skill_type']

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

job_titles_in_data = df['category_code'].map(category_to_job)
job_titles = job_titles_in_data.unique()

col1, col2, col3 = st.columns(3)

with col1:
     job_title = st.selectbox('Select job title:', job_titles)
     job_code = list(category_to_job.keys())[list(category_to_job.values()).index(job_title)]

with col2:  
     cat2_filter = st.selectbox('Select level of job:', df['job_level'].unique())  

with col3:
    cat3_filter = st.selectbox('Select Skill type: ', df['skill_type'].unique())

filtered_df = df[(df['category_code'] == job_code) &  
                (df['job_level'] == cat2_filter) &
                (df['skill_type'] == cat3_filter)]


if len(filtered_df) > 0:
    skills = filtered_df["Skill"].value_counts().nlargest(10)

    fig = px.bar(skills, x=skills.index, y=skills.values, width=1400, height=600)

    fig.update_layout(
        title="Top Skills",
        xaxis_title=f"{cat3_filter}",
        yaxis_title="Number of Occurrences in Job Descriptions",
    )
    st.write(fig)

    from wordcloud import WordCloud

    text = " ".join(skills.index)
    wc = WordCloud(width=1400, height=600).generate(text)
    st.image(wc.to_array())
else:
    st.text("No Data Available for this combination")

