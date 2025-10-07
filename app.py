import streamlit as st
import sys
import os
from dotenv import load_dotenv

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
dotenv_path = os.path.join(current_dir, 'api', '.env')

load_dotenv(dotenv_path=dotenv_path)

PRODUCTION = os.getenv("PRODUCTION")

if PRODUCTION == "True":
    API_BASE = "http://api:8000"
else:
    API_BASE = "http://localhost:8000"

print(API_BASE)
print(PRODUCTION)


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


# Styling för Take quiz och Create quiz knapparna. 
# !!OBS!! byter du färgen på en så byts båda...fattar inte varför
st.markdown("""
<style>
/* TAKE QUIZ knapp */
div.stButton > button:first-child {
    font-size: 20px;
    padding: 20px;
    background-color: #4CAF50;
    color: white;
    border-radius: 10px;
    border: none;
    cursor: pointer;
    transition: 0.2s;
}
div.stButton > button:first-child:hover {
    background-color: #43A047;
}

/* CREATE QUIZ knapp */
div.stButton > button:nth-child(2) {
    font-size: 20px;
    padding: 20px;
    background-color: #2196F3;
    color: white;
    border-radius: 10px;
    border: none;
    cursor: pointer;
    transition: 0.2s;
}
div.stButton > button:nth-child(2):hover {
    background-color: #1976D2;
}
</style>
""", unsafe_allow_html=True)








# Main app content
def main():
    clickable_logo()
    st.markdown("""
    <div style='text-align: center; padding: 2rem;'>
        <p style='font-size: 1.2rem; color: #666; margin-bottom: 2rem;'>Welcome to your quiz application!</p>
    </div>
    """, unsafe_allow_html=True)
    

    
    


    

    # Create two columns for the clickable boxes (takeQuiz, createQuiz).
    col1, col2 = st.columns(2)

    with col1:
        if st.button("📘 Take Quiz", key="take_quiz_button", use_container_width=True):
            st.success("ska navigera till Take Quiz-sidan sen...")  # Replace with navigation logic

    with col2:
        if st.button("✏️ Create Quiz", key="create_quiz_button", use_container_width=True):
            st.session_state["current_page"] = "create_quiz"
            st.rerun()

# Förklaring till koden "with col2:" ovan:
#           När du klickar på en knapp sparas ett “tillstånd” (state) i Streamlit: st.session_state["current_page"] = "create_quiz".
#           Sedan körs st.experimental_rerun(), vilket betyder att appen startar om sig själv direkt.           



    # Flyttade denna ner hit så att den ligger under TakeQuiz och CreateQuiz knapparna.
    st.info("👈 Use the sidebar to navigate between different pages of the application.")


# Förklaring till koden nedan:
# 1. Detta skapar en variabel i minnet som heter "current_page". Den börjar som "home".
# 2. If-statements kontrollerar variabeln för att se vilken sida vi "vill till".
# 3. "st.switch_page" navigerar till den sidan variabeln är uppdaterad till.

if __name__ == "__main__":
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "home"

    if st.session_state["current_page"] == "create_quiz":
        st.switch_page("pages/1_Create_Quiz.py")

    elif st.session_state["current_page"] == "take_quiz":
        st.switch_page("pages/2_Take_Quiz.py")

    else:
        main() 




