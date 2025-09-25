import streamlit as st
import pathlib
import requests

API_BASE = "http://localhost:8000"

QUIZ_DETAIL_URL = lambda qid: f"{API_BASE}/quizzes/quizzes/{qid}"  # try without trailing slash first


quiz_id = st.session_state.get("selected_quiz_id")

def delete_quiz(quiz_id: int):
    try:
        res = requests.delete(f"{API_BASE}/quizzes/quizzes/{quiz_id}/")
        if res.ok:
            return True
        else:
            st.error(f"Failed to delete quiz: {res.status_code} — {res.text}")
            return False
    except Exception as e:
        st.error(f"Error deleting quiz: {e}")
        return False

# Function to load CSS from the 'pages' folder
def load_css(file_path):
    with open(file_path) as f:
        st.html(f"<style>{f.read()}</style>")

# Load the external CSS
css_path = pathlib.Path("pages/styles/5_Preview.css")
load_css(css_path)


st.markdown("<h1 style='text-align: center; color: #88bde6;'>📘 BrainTap</h1>", unsafe_allow_html=True)

st.markdown("---")

col11, col12, col13 = st.columns([1, 1, 1])

with col12:
    if quiz_id:
        r = requests.get(f"{API_BASE}/quizzes/quizzes/{quiz_id}")
        if r.ok:
            quiz = r.json()
            st.markdown(
                f"""
                <div class="quiz-preview-box">
                    <h2 class="quiz-title">{quiz['quiz_name']}</h2>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.error("Quiz not found")
    else:
        st.warning("No quiz selected. Go back and pick one.")



col21, col22, col23 = st.columns([1, 1, 1])

with col21:
    if st.button("Remove", key="remove"):
        if quiz_id:
            if delete_quiz(quiz_id):
                st.success("✅ Quiz deleted!")
                # Clear state so preview doesn't keep stale ID
                st.session_state.pop("selected_quiz_id", None)
                # Go back to Home page
                st.switch_page("pages/0_Home_Page.py")
        else:
            st.warning("No quiz selected.")


with col22:
    if st.button("Edit", key="edit"):
        st.session_state["selected_quiz_id"] = quiz["id"]
        st.switch_page("pages/1_Create_Quiz.py")

with col23:
    if st.button("Run Quiz", key="run"):
        st.info("Run Quiz button pressed (not implemented yet).")



