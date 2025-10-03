import streamlit as st

def clickable_logo():
    """Display a clickable logo that returns to home page when clicked"""
    
    # Create a clickable logo using a custom button with unique styling
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📘 BrainTap", key="brainTap_logo_nav_button", help="Click to return to home page", use_container_width=True):
            st.switch_page("pages/0_Home_Page.py")
    

