import streamlit as st
import pandas as pd
import altair as alt

import numpy as np

st.title("Map")

df = pd.read_parquet('Data/Indeed/merged.parquet', columns=['latitude', 'longitude'])

df = df.dropna()

st.map(df, size=20, color='#0044ff')