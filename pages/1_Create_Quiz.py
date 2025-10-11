from __future__ import annotations
from rel.crud_operations import ResourceClient
from pages.styles.logo import clickable_logo
from pages.styles.logo import clickable_logo, load_css as load_logo_css
from state import init_state,reset_editor
from pathlib import Path
from app import API_BASE
import streamlit as st
import requests
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
quiz_table = ResourceClient(base_url=API_BASE, endpoint_path="/quizzes/")
quiz_id = st.session_state.get("selected_quiz_id")

ss = st.session_state
if "quiz_tuples" not in ss:
    ss.quiz_tuples = []
if "is_editing" not in ss:
    ss.is_editing = False
if "cursor" not in ss:
    ss.cursor = 0
if "refresh_widgets" not in ss:
    ss.refresh_widgets = True  

               
# Change button type based on edit mode and question count
# If in edit mode and number of questions unchanged -> primary, otherwise secondary
is_edit_mode = ss.get("selected_quiz_id") is not None
original_count = ss.get("original_question_count", 0)
current_count = len(ss.quiz_tuples)

def editor_changed() -> bool:
    if not ss.get("is_editing"):
        return False
    qtext, (v0, v1, v2, v3), correct_idx = get_editor_values()
    orig = ss.get("editing", {})
    orig_text = orig.get("text", "")
    orig_idx = orig.get("correct_index", 0)
    # pad/crop to 4 choices
    orig_choices = list(orig.get("choices", ["", "", "", ""]))[:4]
    while len(orig_choices) < 4:
        orig_choices.append("")
    return (
        qtext != orig_text
        or correct_idx != orig_idx
        or [v0, v1, v2, v3] != orig_choices
    )



st.set_page_config(page_title="Create Quiz – Add Questions", layout="wide")


def load_css():
    here = Path(__file__).parent
    for p in (here / "styles" / "create_quiz.css", here.parent / "styles" / "create_quiz.css"):
        if p.is_file():
            st.markdown(f"<style>{p.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)
            return


def set_widgets_from_editing():
    """Copy ss.editing -> widget keys so widgets show desired values."""
    e = ss.editing
    st.session_state["editing_text"] = e.get("text", "")
    st.session_state["editing_correct_index"] = e.get("correct_index", 0)
    ch = e.get("choices", ["", "", "", ""])
    for i in range(4):
        st.session_state[f"choice{i}"] = ch[i] if i < len(ch) else ""


def get_editor_values():
    """Read current widget values -> return tuple(qtext, (v0..v3), correct_idx)."""
    qtext = st.session_state.get("editing_text", "")
    correct_idx = st.session_state.get("editing_correct_index", 0)
    v0 = st.session_state.get("choice0", "")
    v1 = st.session_state.get("choice1", "")
    v2 = st.session_state.get("choice2", "")
    v3 = st.session_state.get("choice3", "")
    return qtext, (v0, v1, v2, v3), correct_idx


def page_add_questions():
    load_css()
    st.markdown('<div id="create-quiz">', unsafe_allow_html=True)
    
    # Show clickable logo
    clickable_logo()
    


    # Show quiz name
    quiz_name = ss.get("new_quiz_name") or ss.get("quiz_name", "New Quiz")
    if "_" in quiz_name and quiz_name.split("_")[-1].isdigit():
        clean_name = "_".join(quiz_name.split("_")[:-1])
    else:
        clean_name = quiz_name
    st.title(f" {clean_name}")

    if "editing" not in ss:
        reset_editor()
        ss.refresh_widgets = True

    if ss.refresh_widgets:
        if ss.get("is_editing", False):
            set_widgets_from_editing()
        else:
            for key in ["editing_text", "choice0", "choice1", "choice2", "choice3", "editing_correct_index"]:
                st.session_state[key] = "" if not key.endswith("index") else 0
                ss.refresh_widgets = False

    left, main, right = st.columns([1, 3, 1])

    with main:
        st.markdown('<div class="question-header">WRITE YOUR QUESTION</div>', unsafe_allow_html=True)

        st.text_area("Question Text", key="editing_text", height=120, placeholder="Type your question here…")
        st.radio("Correct Answer", options=[0, 1, 2, 3], key="editing_correct_index", horizontal=True)

        r1c1, r1c2 = st.columns(2, gap="large")
        with r1c1:
            st.text_input("Choice 1", key="choice0", placeholder="Enter first choice")
        with r1c2:
            st.text_input("Choice 2", key="choice1", placeholder="Enter second choice")

        r2c1, r2c2 = st.columns(2, gap="large")
        with r2c1:
            st.text_input("Choice 3", key="choice2", placeholder="Enter third choice")
        with r2c2:
            st.text_input("Choice 4", key="choice3", placeholder="Enter fourth choice")

    col_left, col_right = st.columns([1.2, 0.2])

    # PUBLISH
    with col_left:
        if "publishing" not in ss:
            ss.publishing = False
            ss.publish_start_time = None
            ss.last_published_quiz = None
        
        # Reset publishing state if it's been too long (30 seconds timeout)
        if ss.publishing and ss.publish_start_time:
            import time
            if time.time() - ss.publish_start_time > 30:
                ss.publishing = False
                ss.publish_start_time = None
                #st.warning("⏰ Publishing timeout. Please try again.")
        
        if current_count < 1:
            button_type = "primary"
        elif is_edit_mode and current_count == original_count:
            button_type = "primary"
        elif not editor_changed():
            button_type = "primary"
        else:
            button_type = "secondary"
        
        if st.button("PUBLISH QUIZ", disabled=ss.publishing, type=button_type):
            if len(ss.quiz_tuples) < 1:
                st.error("You must add at least 1 question.")
            elif ss.publishing:
                st.warning("Please wait, quiz is being published...")
            elif ss.last_published_quiz == ss.quiz_tuples:
                st.warning("This quiz was already published. Add more questions or make changes before publishing again.")
            else:
                # Set publishing state to prevent double-clicks
                import time
                ss.publishing = True
                ss.publish_start_time = time.time()
                st.info("Publishing quiz... Please wait.")
                
                # Check if we're editing an existing quiz or creating a new one
                quiz_id = ss.get("selected_quiz_id")

                if quiz_id:
                    quiz_name = ss.get("quiz_name", "Untitled Quiz")
                    quiz_payload = {
                        "quiz_name": quiz_name,
                        "number_question": len(ss.quiz_tuples),
                        "creator_id": ss.get("creator_id", 1),
                    }

                    try:
                        quiz_table.update(quiz_id, quiz_payload)
                        new_quiz_id = quiz_id  # Use existing ID

                        # Delete existing questions first
                        # question_table.delete(quiz_id)
                        requests.delete(f"{API_BASE}/quizzes/{quiz_id}/questions")

                    except requests.exceptions.RequestException as e:
                        st.error(f" Failed to update quiz: {e}")
                        return
                        
                else:
                    # CREATING NEW QUIZ
                    base_name = ss.get("new_quiz_name") or ss.get("quiz_name", "Untitled Quiz")
                    if "quiz_creation_id" not in ss:
                        ss.quiz_creation_id = int(time.time() * 1000)  # milliseconds for uniqueness
                    unique_name = f"{base_name}_{ss.quiz_creation_id}"
                    
                    quiz_payload = {
                        "quiz_name": unique_name,
                        "is_active": 1,
                        "number_question": len(ss.quiz_tuples),
                        "creator_id": ss.get("creator_id", 1),
                    }
                    
                    try:
                        quiz_data = quiz_table.create(quiz_payload)
                        new_quiz_id = quiz_data["id"]
                        
                    except requests.exceptions.RequestException as e:
                        st.error(f" Failed to create quiz: {e}")
                        return
                
                try:
                    question_table = ResourceClient(base_url=API_BASE, endpoint_path=f"quizzes/{new_quiz_id}/questions")

                    # Add all questions
                    questions_added = 0
                    for (qtext, choices, correct_idx) in ss.quiz_tuples:
                        question_payload = {
                            "question_text": qtext,
                            "choice_1": choices[0],
                            "choice_2": choices[1],
                            "choice_3": choices[2],
                            "choice_4": choices[3],
                            "answer": correct_idx,
                        }
                        question_table.create(question_payload)
                        questions_added += 1

                    # Success - clear state and reset
                    action = "updated" if quiz_id else "created"
                    st.success(f" Quiz {action} successfully! ID: {new_quiz_id} ({questions_added} questions)")
                    st.cache_data.clear()
                    for key in ["quiz_loaded", "fetched_quiz"]:
                        if key in st.session_state:
                            del st.session_state[key]
                            
                            
                    ss.last_published_quiz = ss.quiz_tuples.copy()  
                    ss.quiz_tuples = []
                    ss.publishing = False
                    ss.publish_start_time = None
                    ss.new_quiz_name = None  
                    ss.create_open = False  
                    ss.selected_quiz_id = None  
                    ss.quiz_loaded = False  
                    reset_editor()
                    ss.is_editing = False
                    ss.refresh_widgets = True
                    st.switch_page("pages/0_Home_Page.py")

                except requests.exceptions.RequestException as e:
                    ss.publishing = False
                    ss.publish_start_time = None
                    st.error(f" Network error: {e}")
                except Exception as e:
                    ss.publishing = False
                    ss.publish_start_time = None
                    st.error(f" Failed to publish quiz: {e}")

    # ADD / 
    with col_right:
        qtext, (v0, v1, v2, v3), correct_idx = get_editor_values()

        # ADD
        if not ss.is_editing:
            if st.button("ADD", type="primary"):
                ss.quiz_tuples.append((qtext, tuple([v0, v1, v2, v3]), correct_idx))
                ss.last_published_quiz = None  
                st.success("Question added!")
                reset_editor()
                ss.is_editing = False
                ss.refresh_widgets = True
                st.rerun()

        # UPDATE
        if ss.is_editing:
            update_btn_type = "secondary" if editor_changed() else "primary"
            if st.button("UPDATE", type=update_btn_type):
                if 0 <= ss.cursor < len(ss.quiz_tuples):
                    qtext, (v0, v1, v2, v3), correct_idx = get_editor_values()
                    ss.quiz_tuples[ss.cursor] = (qtext, (v0, v1, v2, v3), correct_idx)
                    st.success("Question updated!")
                reset_editor()
                ss.is_editing = False
                ss.refresh_widgets = True
                st.rerun()


    total = len(ss.get("quiz_tuples", []))
    st.caption(f"Total questions: {total}")

    # SAVED QUESTIONS
    if ss.quiz_tuples:
        st.divider()
        st.header("Questions:")

        for i, (qtext, choices, correct_idx) in enumerate(ss.quiz_tuples):
            col_q, col_edit, col_delete = st.columns([3, 1, 1])

            # Show as a button to load into editor
            with col_q:
                if st.button(f"Fråga {i+1}: {qtext}", key=f"show_q_{i}", type="tertiary"):
                    ss.editing = {"text": qtext, "choices": list(choices), "correct_index": correct_idx}
                    ss.cursor = i
                    ss.is_editing = True
                    ss.refresh_widgets = True
                    st.rerun()

            with col_edit:
                if st.button(" Edit", key=f"edit{i}", type="tertiary"):
                    ss.editing = {"text": qtext, "choices": list(choices), "correct_index": correct_idx}
                    ss.cursor = i
                    ss.is_editing = True
                    ss.refresh_widgets = True
                    st.rerun()

            with col_delete:
                if st.button(" Delete", key=f"delete{i}", type="tertiary"):
                    ss.quiz_tuples.pop(i)
                    st.success(f"Question {i + 1} deleted.")
                    reset_editor()
                    ss.is_editing = False
                    ss.refresh_widgets = True
                    st.rerun()

# ===  ===  ===  ===  ===  ===  ===  ===  ===  ===  ===  ===  ===  ===  ===  ===  ===  ===  ===  ===  
# ===  ===  ===  ===  ===  ===  ===  ===  ===  ===  ===  ===  ===  ===  ===  ===  ===  ===  ===  ===  
# ===  ===  ===  ===  ===  ===  ===  ===  ===  ===  ===  ===  ===  ===  ===  ===  ===  ===  ===  ===  


# Init + optional preload from backend
init_state()

# Load existing quiz data if editing
if quiz_id and "quiz_loaded" not in st.session_state:
    quiz_data = quiz_table.get_one(quiz_id)
    if quiz_data:
        st.session_state.quiz_name = quiz_data.get("quiz_name", "Untitled Quiz")
        st.session_state.creator_id = quiz_data.get("creator_id", 1)
        questions = quiz_data.get("questions", [])
        st.session_state.quiz_tuples = [
            (q["question_text"], (q["choice_1"], q["choice_2"], q["choice_3"], q["choice_4"]), q["answer"]) for q in questions
        ]
        st.session_state.original_question_count = len(questions)  # Track original count
        st.session_state.quiz_loaded = True

page_add_questions()
