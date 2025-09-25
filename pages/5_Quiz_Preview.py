import streamlit as st
import pathlib

# Function to load CSS from the 'pages' folder
def load_css(file_path):
    with open(file_path) as f:
        st.html(f"<style>{f.read()}</style>")

# Load the external CSS
css_path = pathlib.Path("pages/styles/5_Preview.css")
load_css(css_path)


st.markdown("<h1 style='text-align: center; color: #88bde6;'>📘 BrainTap</h1>", unsafe_allow_html=True)

st.markdown("---")

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("Remove", key="remove"):
        st.info("Remove button pressed (not implemented yet).")

with col2:
    if st.button("Edit", key="edit"):
        st.info("Edit button pressed (not implemented yet).")

with col3:
    if st.button("Run Quiz", key="run"):
        st.info("Run Quiz button pressed (not implemented yet).")