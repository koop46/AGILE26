import streamlit as st
import pathlib

# Function to load CSS from the 'pages' folder
def load_css(file_path):
    with open(file_path) as f:
        st.html(f"<style>{f.read()}</style>")

# Load the external CSS
css_path = pathlib.Path("pages/styles/4_Name_Quiz_Style.css")
load_css(css_path)

st.markdown("<h1 style='text-align: center; color: #88bde6;'>📘 BrainTap</h1>", unsafe_allow_html=True)

st.markdown("---")

quiz_name = st.text_input("", placeholder="Name Your Quiz", key="textInput")

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("Back", key="back"):
        st.info("Back button pressed (not implemented yet).")

with col3:
    if st.button("Save", key="save"):
        if quiz_name.strip() != "":
            st.success(f"Quiz '{quiz_name}' has been saved successfully!")
        else:
            st.warning("Please enter a name for your quiz before saving!")


