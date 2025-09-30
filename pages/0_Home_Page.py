import streamlit as st
import requests

# --- Session state init ---
if "create_open" not in st.session_state:
    st.session_state.create_open = False
if "create_quiz_name" not in st.session_state:
    st.session_state.create_quiz_name = ""

API_BASE = "http://localhost:8000"  # FastAPI base URL
response = requests.get("http://localhost:8000/quizzes")  # <-- FIXED
QUIZZES_LIST_URL    = f"{API_BASE}/quizzes/quizzes/"        # GET
QUIZ_CREATE_URL     = f"{API_BASE}/quizzes/quizzes/"        # POST
QUESTION_CREATE_URL = f"{API_BASE}/quizzes/questions/"      # POST
QUIZ_DELETE_URL     = lambda qid: f"{API_BASE}/quizzes/quizzes/{qid}/"  # DELETE

# Import CSS styles
def load_css():
    with open("pages/styles/0_Home_Page.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if response.status_code == 200:
    quizzes = response.json()
else:
    quizzes = []

# Gets all available Quizes
def fetch_quizzes():
    try:
        r = requests.get(f"{API_BASE}/quizzes/quizzes/")  # NOTE: trailing slash
        r.raise_for_status()
        return r.json()
    except Exception as e:
        st.error(f"Failed to fetch quizzes: {e}")
        return []

# Deletes all available Quizes
def delete_all_quizzes():
    quizzes = fetch_quizzes()
    deleted = 0
    for q in quizzes:
        res = requests.delete(f"{API_BASE}/quizzes/quizzes/{q['id']}/")
        if res.ok:
            deleted += 1
    return deleted


load_css()

st.markdown("<h1 style='text-align: center; color: #88bde6;'>📘 BrainTap</h1>", unsafe_allow_html=True)

st.markdown("---")

# Create quiz popup window
@st.dialog("Create a new quiz")
def create_quiz_dialog():
    name = st.text_input("Quiz name", key="create_quiz_name")
    if st.button("Create"):
        if not name.strip():
            st.warning("Please enter a name.")
            return
        payload = {"quiz_name": name.strip(), "number_question": 0, "creator_id": 0}
        res = requests.post(QUIZ_CREATE_URL, json=payload)
        if res.ok:
            st.success("✅ Quiz created!")
            st.session_state["selected_quiz_id"] = quiz["id"]
            st.session_state.create_open = False
            st.switch_page("pages/1_Create_Quiz.py")
            st.rerun()
        else:
            st.error(f"❌ {res.text}")

quizzes = fetch_quizzes()

# Second Row ---------------------------------------------------------------------------
r2c1, r2c2, r2c3 = st.columns([1,1,1])

with r2c2:
# Create Quiz button
    if st.button("Create a Quiz", key="main_quiz_button", type="primary"):
        st.session_state.create_open = True

    if st.session_state.create_open:
        create_quiz_dialog()


# Third Row ---------------------------------------------------------------------------
r3c1, r3c2, r3c3 = st.columns([0.2,3,0.2])



with r2c2:
    if quizzes:
        for quiz in quizzes:
            with st.container():
                col_a, col_b = st.columns([5, 1])
                with col_a:
                    st.write(f"{quiz['quiz_name']}")
                with col_b:
                    if st.button("Take", key=f"take_{quiz['id']}"):
                        # Save quiz id in session state
                        st.session_state["selected_quiz_id"] = quiz["id"]
                        # Switch to Preview page
                        st.switch_page("pages/5_Quiz_Preview.py")
    else:
        st.info("No quizzes found yet. Create one to get started!")

load_css()