import streamlit as st
import pandas as pd
import plotly.express as px
import re

df = pd.read_csv(r'Data/USA_Jobs_Data.csv')

st.set_page_config(layout="wide")
st.title("🏛️ Government Jobs")

col1, col2, col3 = st.columns(3)

with col2:
      selected_keyword = st.selectbox("What is your desired job title?", df['search_keyword'].unique())

# Filter DataFrame based on selected keyword
filtered_df = df[df['search_keyword'] == selected_keyword]

# Group by department and count the occurrences
department_counts = filtered_df['department'].value_counts()

# Sort the values in descending order
department_counts = department_counts.sort_values(ascending=True)

# Select only the top 10 departments
top_10_departments = department_counts.nlargest(10)

# Sort the top 10 departments in descending order
top_10_departments = top_10_departments.sort_values(ascending=False)

# Create a new DataFrame for plotting
plot_df = pd.DataFrame({'Department': top_10_departments.index, 'Number of Jobs': top_10_departments.values})

# Create the plot using the sorted DataFrame
fig = px.bar(plot_df, x='Department', y='Number of Jobs', title=f'Top 10 Job Count for {selected_keyword}',
             labels={'Department': 'Department', 'Number of Jobs': 'Number of Jobs'},
             category_orders={'Department': plot_df['Department'].values}, width=1400, height=800)

# Update the x-axis label
fig.update_layout(xaxis_title='Department')

# Show the figure
st.plotly_chart(fig)