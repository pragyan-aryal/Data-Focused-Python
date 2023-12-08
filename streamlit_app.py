import streamlit as st
st.title("CareerCompass")

jobs_list = ["Software Engineer", "Data Analyst", "Product Manager", "Project Manager","Business Analyst", "Data Engineer", "Mechanical Engineer", "CAE Engineer", "FEA Engineer", "Civil Engineer"]
job_title = st.selectbox("Job Title", options = jobs_list)

years_ex = st.slider("How many years of experience do you have?", 0, 10)
if years_ex <= 3:
   st.write("You are considered as entry level professional in the job market.")
elif years_ex > 3 and years_ex <=7:
   st.write("You are considered as mid level professional in the job market.")
else:
   st.write("You are considered as senior level professional in the job market.")
  
need_h1 = st.checkbox("Do you need sponsorship now or in future?")
if need_h1:
   button1 = st.button("Next1")
