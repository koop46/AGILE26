import streamlit as st

def load_css():
    with open("pages/styles/logo.css", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def clickable_logo():
    """Display the logo in the sidebar"""
    st.logo(
        "pages/styles/Logo_Large.png"
    )