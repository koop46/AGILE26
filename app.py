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

### === Hämtar css filen från styles-mappen med styling för app.py-sidan. === ###
def load_css():
    with open("pages/styles/app_page.css", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)





#### === Take Quiz pop-up dialog === ####
@st.dialog("Take a Quiz")
def show_take_quiz_dialog():
    # Fält för att skriva in QuizID och Username.
    quiz_input = st.text_input("Enter Quiz ID", key="take_quiz_input")
    username_input = st.text_input("Enter desired username", key="take_quiz_username_input")

    # Flagga för att tala om ifall vi ska visa en varning
    show_warning = False
    
    col1, col2 = st.columns(2)
    with col2:
        if st.button("Start Quiz", key="start_quiz_button", use_container_width=True):
            # Säkerställer att båda fälten är ifyllda (.strip tar bort whitespace)
            if not quiz_input.strip() or not username_input.strip():
                show_warning = True
            else:
                # Allt OK -- Spara info och byt sida
                # Spara användarens val i session_state
                st.session_state["selected_quiz_id_or_name"] = quiz_input.strip()
                st.session_state["username"] = username_input.strip()
                st.switch_page("pages/2_Take_Quiz.py")

    # Visa varningen efter layouten, så inte Cancel-knappen försvinner.
    if show_warning:
        st.warning("Please fill in both fields before starting a quiz.")





#### ==== Main app content ==== ####
def main():

    # --- Logga och text --- #
    load_css()
    clickable_logo()
    st.markdown("""
    <div style='text-align: center; padding: 2rem;'>
        <p style='font-size: 1.2rem; color: #666; margin-bottom: 2rem;'>Welcome to your quiz application!</p>
    </div>
    """, unsafe_allow_html=True)


    
    # --- Knapparna Create Quiz och Take Quiz --- #
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📘 Take Quiz", key="take_quiz_button", use_container_width=True):
            show_take_quiz_dialog()
    with col2:
        if st.button("✏️ Create Quiz", key="create_quiz_button", use_container_width=True):
            st.switch_page("pages/0_Home_Page.py")


    # --- Info-text längst ner --- #
    st.info("👈 Use the sidebar to navigate between different pages of the application.")


if __name__ == "__main__":
    main()





