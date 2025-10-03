import os
import requests
import streamlit as st
from dotenv import load_dotenv


# --- Session state init ---
ss = st.session_state
ss.setdefault("create_open", False)
ss.setdefault("create_quiz_name", "")


load_dotenv()

PRODUCTION = os.getenv("PRODUCTION")

if PRODUCTION == True:
    API_BASE = "http://api:8000"
else:
    API_BASE = "http://localhost:8000"


#API_BASE = "http://localhost:8000"  # FastAPI base URL
response = requests.get("http://localhost:8000/quizzes")  # <-- FIXED
QUIZZES_LIST_URL    = f"{API_BASE}/quizzes/quizzes/"        # GET
QUIZ_CREATE_URL     = f"{API_BASE}/quizzes/quizzes/"        # POST
QUESTION_CREATE_URL = f"{API_BASE}/quizzes/questions/"      # POST
QUIZ_DELETE_URL     = lambda qid: f"{API_BASE}/quizzes/quizzes/{qid}/"  # DELETE

# CSS
def load_css():
    with open("pages/styles/0_Home_Page.css", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def fetch_quizzes():
    try:
        r = requests.get(QUIZZES_LIST_URL)  # correct endpoint
        r.raise_for_status()
        data = r.json()
        return data if isinstance(data, list) else []
    except Exception as e:
        st.error(f"Failed to fetch quizzes: {e}")
        return []

def delete_all_quizzes():
    quizzes = fetch_quizzes()
    deleted = 0
    for q in quizzes:
        res = requests.delete(QUIZ_DELETE_URL(q["id"]))
        if res.ok:
            deleted += 1
    return deleted

def clean_quiz_name_for_display(quiz_name):
    """Remove timestamp suffix from quiz name for display purposes"""
    if "_" in quiz_name:
        # Split by underscore and check if last part is a timestamp (all digits)
        parts = quiz_name.split("_")
        if len(parts) > 1 and parts[-1].isdigit():
            # Remove the last part (timestamp)
            return "_".join(parts[:-1])
    return quiz_name


load_css()
clickable_logo()
st.markdown("---")

@st.dialog("Create a new quiz")
def create_quiz_dialog():
    name = st.text_input("Quiz name", key="create_quiz_name")
    if st.button("Create"):
        if not name.strip():
            st.warning("Please enter a name.")
            return
        
        # Store the quiz name for later use, don't create quiz yet
        st.session_state["new_quiz_name"] = name.strip()
        st.session_state["selected_quiz_id"] = None  # No existing quiz
        st.session_state.create_open = False
        st.success("✅ Ready to create quiz!")
        st.switch_page("pages/1_Create_Quiz.py")

# Centered Create Quiz button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("Create a Quiz", key="main_quiz_button", type="primary", use_container_width=True):
        st.session_state.create_open = True
        st.rerun()  # Rerun to show the dialog immediately

# Show dialog only if create_open is True
if st.session_state.create_open:
    create_quiz_dialog()

# List quizzes
quizzes = fetch_quizzes()
c1, c2, c3 = st.columns([0.2, 3, 0.2])
with c2:
    if quizzes:
        st.subheader("Available Quizzes")
        for quiz in quizzes:
            raw_title = quiz.get("quiz_name", "Untitled Quiz")
            clean_title = clean_quiz_name_for_display(raw_title)
            qid = quiz.get("id")
            col_a, col_b, col_c = st.columns([4, 1, 1])
            with col_a:
                st.write(f"• {clean_title}")
            with col_b:
                if qid is not None and st.button("Edit", key=f"edit_{qid}"):
                    st.session_state["selected_quiz_id"] = qid
                    st.switch_page("pages/1_Create_Quiz.py")
            with col_c:
                if qid is not None and st.button("Take", key=f"take_{qid}"):
                    st.session_state["selected_quiz_id"] = qid
                    st.switch_page("pages/5_Quiz_Preview.py")
    else:
        st.info("No quizzes. Create one to get started!")
