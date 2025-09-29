import streamlit as st
import pathlib
import requests

API_BASE = "http://localhost:8000"

QUIZ_DETAIL_URL = lambda qid: f"{API_BASE}/quizzes/quizzes/{qid}"  # try without trailing slash first


quiz_id = st.session_state.get("selected_quiz_id")

st.set_page_config(page_title="Quiz Preview", layout="centered")

ss = st.session_state          # <— alias so 'ss' exists

quiz = [
    ("What is the capital of France?", ("Paris", "London", "Berlin", "Rome"), 0),
]
if "editing" not in ss:
    q, opts, rid = quiz[0]
    ss.editing = {"text": q, "choices": list(opts), "correct_index": rid}
    ss.dirty = False

e = ss.editing


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

r1c1, r1c2, r1c3 = st.columns([0.2, 1, 0.2])

with r1c2:
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

r2c1, r2c2, r2c3 = st.columns([0.2, 1, 0.2])
with r2c2:
    if quiz_id:
        r = requests.get(f"{API_BASE}/quizzes/quizzes/{quiz_id}")
        if r.ok:
            quiz = r.json()
            st.markdown(
                f"""
                <div class="question-preview-box">
                    <h3 class="quiz-question">{"hej"}</h3>
                </div>
                """,
                unsafe_allow_html=True
            )

def show_choice(i, placeholder):
    txt = e["choices"][i] or placeholder
    badge = "ABCD"[i]  # or symbols ▲◆●■
    st.markdown(
        f"""
        <div class="answers-preview-box {'correct' if e['correct_index'] == i else ''}">
            <div class="choice-badge">{badge}</div>
            <h3 class="quiz-choice">{txt}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

# ---- layout (2x2) ----
r3c1, r3c2 = st.columns(2, gap="small")
with r3c1: show_choice(0, "Choice 1")
with r3c2: show_choice(1, "Choice 2")

r4c1, r4c2 = st.columns(2, gap="small")
with r4c1: show_choice(2, "Choice 3")
with r4c2: show_choice(3, "Choice 4")




r5c1, r5c2, r5c3 = st.columns([1, 1, 1])

with r5c1:
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


with r5c2:
    if st.button("Edit", key="edit"):
        st.session_state["selected_quiz_id"] = quiz["id"]
        st.switch_page("pages/1_Create_Quiz.py")

with r5c3:
    if st.button("Run Quiz", key="run"):
        st.info("Run Quiz button pressed (not implemented yet).")



