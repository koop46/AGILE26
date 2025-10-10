from rel.crud_operations import ResourceClient
from pages.styles.logo import clickable_logo
from app import API_BASE
import streamlit as st
import pathlib
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
quiz_table = ResourceClient(base_url=API_BASE, endpoint_path="/quizzes/")
quiz_id = st.session_state.get("selected_quiz_id")
st.set_page_config(page_title="Quiz Preview", layout="centered")
ss = st.session_state




# Initialize editing state if not exists
if "editing" not in ss:
    ss.editing = {"text": "", "choices": ["", "", "", ""], "correct_index": 0}
    ss.dirty = False


# Function to load CSS from the 'pages' folder
def load_css(file_path):
    with open(file_path) as f:
        st.html(f"<style>{f.read()}</style>")


# ===  ===  ===  ===  ===  ===  ===  ===  ===  ===  ===  ===  ===  ===  ===  ===  ===  ===  ===  ===  
# ===  ===  ===  ===  ===  ===  ===  ===  ===  ===  ===  ===  ===  ===  ===  ===  ===  ===  ===  ===  
# ===  ===  ===  ===  ===  ===  ===  ===  ===  ===  ===  ===  ===  ===  ===  ===  ===  ===  ===  ===  


# Load the external CSS
css_path = pathlib.Path("pages/styles/5_Preview.css")
load_css(css_path)


clickable_logo()

@st.dialog("Are you sure you want to delete the quiz?")
def create_quiz_dialog():
    if st.button("REMOVE"):
        if quiz_id:
            if quiz_table.delete(quiz_id):
                st.success("✅ Quiz deleted!")
                # Clear state so preview doesn't keep stale ID
                st.session_state.pop("selected_quiz_id", None)
                # Go back to Home page
                st.switch_page("pages/0_Home_Page.py")
        else:
            st.warning("No quiz to delete.")
        
        # Store the quiz name for later use, don't create quiz yet
        st.session_state["new_quiz_name"] = name.strip()
        st.session_state["selected_quiz_id"] = None  # No existing quiz
        st.session_state.create_open = False
        st.success("✅ Ready to create quiz!")
        st.switch_page("pages/1_Create_Quiz.py")



r1c1, r1c2, r1c3 = st.columns([0.2, 1, 0.2])

with r1c2:
    if quiz_id:
        try:
            ### Hämtar ###
            quiz_data = quiz_table.get_one(quiz_id)
                         
            # Clean quiz name for display
            raw_quiz_name = quiz_data.get('quiz_name', 'Untitled Quiz')
            if "_" in raw_quiz_name and raw_quiz_name.split("_")[-1].isdigit():
                clean_quiz_name = "_".join(raw_quiz_name.split("_")[:-1])
            else:
                clean_quiz_name = raw_quiz_name
            
            st.markdown(
                f"""
                <div class="quiz-preview-box">
                    <h2 class="quiz-title">{clean_quiz_name}</h2>
                </div>
                """,
                unsafe_allow_html=True
            )

            #  first question
            questions = quiz_data.get("questions", [])
            if questions:
                first_q = questions[0]
                q_text = first_q.get("question_text", "")
                choices = [
                    first_q.get("choice_1", ""),
                    first_q.get("choice_2", ""),
                    first_q.get("choice_3", ""),
                    first_q.get("choice_4", "")
                ]
                correct_index = first_q.get("answer", 0)

                st.session_state.editing = {
                    "text": q_text,
                    "choices": choices,
                    "correct_index": int(correct_index)
                }
            else:
                st.warning("This quiz has no questions.")
        
        except Exception as e:
            st.error(f"Error loading quiz: {e}")
    else:
        st.warning("No quiz selected. Go back and pick one.")

# render question text
if "editing" in st.session_state:
    e = st.session_state.editing
    r2c1, r2c2, r2c3 = st.columns([0.2, 1, 0.2])
    with r2c2:
        st.markdown(
            f"""
            <div class="question-preview-box">
                <h3 class="quiz-question">{e['text']}</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

    #  render choices
    def show_choice(i, placeholder):
        txt = e["choices"][i] or placeholder
        st.markdown(
            f"""
            <div class="answers-preview-box {'correct' if e['correct_index'] == i else ''}">
                <h3 class="quiz-choice">{txt}</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

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
            if quiz_table.delete(quiz_id):
                st.success(" Quiz deleted!")
                st.session_state.pop("selected_quiz_id", None)
              
                st.switch_page("pages/0_Home_Page.py")
        else:
            st.warning("No quiz selected.")


with r5c2:
    if st.button("Edit", type="primary"):
        if quiz_id:
            st.session_state["selected_quiz_id"] = int(quiz_id)
            st.switch_page("pages/1_Create_Quiz.py")
        else:
            st.warning("No quiz selected.")


with r5c3:
    if st.button("Run Quiz", key="run"):
        if quiz_id:
            for key in list(st.session_state.keys()):
                if key.startswith("choice_"):
                    del st.session_state[key]

            st.session_state.current_question_index = 0
            st.session_state.score = 0
            st.session_state.user_answers = []
            st.session_state.quiz_started = False  

            # Set the selected quiz ID and go to Take Quiz
            st.session_state["selected_quiz_id"] = int(quiz_id)
            st.switch_page("pages/2_Take_Quiz.py")
        else:
            st.warning("No quiz selected.")

            
        #st.info("Run Quiz button pressed (not implemented yet).")
        



