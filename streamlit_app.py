import streamlit as st
from st_pages import Page, show_pages, add_page_title


show_pages(
    [
        Page("streamlit_app.py", "Career Compass", "🚀"),
        Page("pages/H1B.py", "H1B", "🫵"),
        Page("pages/Map.py", "MAP", "😍"),
    ]
)

st.title("Career Compass")
st.sidebar.success("Select a page above")
