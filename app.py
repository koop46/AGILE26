import streamlit as st
import sys
import os

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from pages.styles.logo import clickable_logo

# Page configuration
st.set_page_config(
    page_title="BrainTap Quiz App",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide the default Streamlit menu and footer
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Main app content
def main():
    clickable_logo()
    st.markdown("""
    <div style='text-align: center; padding: 2rem;'>
        <p style='font-size: 1.2rem; color: #666; margin-bottom: 2rem;'>Welcome to your quiz application!</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("👈 Use the sidebar to navigate between different pages of the application.")

if __name__ == "__main__":
    main()
