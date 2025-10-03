from __future__ import annotations
from pathlib import Path
import requests
import streamlit as st
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from pages.styles.logo import clickable_logo
from state import (
    init_state,
    reset_editor,
)

API_BASE = "http://localhost:8000"
quiz_id = st.session_state.get("selected_quiz_id")

ss = st.session_state
if "quiz_tuples" not in ss:
    ss.quiz_tuples = []
if "is_editing" not in ss:
    ss.is_editing = False
if "cursor" not in ss:
    ss.cursor = 0
if "refresh_widgets" not in ss:
    ss.refresh_widgets = True  # force first-time widget init


def fetch_quiz_with_questions(quiz_id: int):
    try:
        r = requests.get(f"{API_BASE}/quizzes/{quiz_id}")
        r.raise_for_status()
        return r.json()
    except Exception as e:
        st.error(f"Failed to fetch quiz {quiz_id}: {e}")
        return None


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
    
    # Show quiz name if available
    quiz_name = ss.get("new_quiz_name") or ss.get("quiz_name", "New Quiz")
    # Clean the name for display (remove timestamp if present)
    if "_" in quiz_name and quiz_name.split("_")[-1].isdigit():
        clean_name = "_".join(quiz_name.split("_")[:-1])
    else:
        clean_name = quiz_name
    st.title(f"📝 {clean_name}")

    # Ensure ss.editing exists
    if "editing" not in ss:
        reset_editor()
        ss.refresh_widgets = True

    # If flagged, push ss.editing into widgets so the form reflects the model
    if ss.refresh_widgets:
        set_widgets_from_editing()
        ss.refresh_widgets = False

    left, main, right = st.columns([1, 3, 1])

    with main:
        st.markdown('<div class="question-header">WRITE YOUR QUESTION</div>', unsafe_allow_html=True)

        # Bind widgets ONLY via keys (no value=/index= so we can programmatically set via st.session_state)
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

    col_left, col_right = st.columns([1.2, 0.1])

    # PUBLISH
    with col_left:
        # Check if we're already publishing to prevent double-clicks
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
                st.warning("⏰ Publishing timeout. Please try again.")
                
        if st.button("PUBLISH QUIZ", disabled=ss.publishing):
            if len(ss.quiz_tuples) < 1:
                st.error("You must add at least 1 question before publishing.")
            elif ss.publishing:
                st.warning("Please wait, quiz is being published...")
            elif ss.last_published_quiz == ss.quiz_tuples:
                st.warning("⚠️ This quiz was already published. Add more questions or make changes before publishing again.")
            else:
                # Set publishing state to prevent double-clicks
                import time
                ss.publishing = True
                ss.publish_start_time = time.time()
                st.info("🔄 Publishing quiz... Please wait.")
                
                # Check if we're editing an existing quiz or creating a new one
                quiz_id = ss.get("selected_quiz_id")
                
                if quiz_id:
                    # EDITING EXISTING QUIZ - Update it
                    quiz_name = ss.get("quiz_name", "Untitled Quiz")
                    quiz_payload = {
                        "quiz_name": quiz_name,
                        "number_question": len(ss.quiz_tuples),
                        "creator_id": ss.get("creator_id", 1),
                    }
                    
                    try:
                        # Update the existing quiz
                        r = requests.put(f"{API_BASE}/quizzes/{quiz_id}", json=quiz_payload)
                        r.raise_for_status()
                        quiz_data = r.json()
                        new_quiz_id = quiz_id  # Use existing ID
                        
                        # Delete existing questions first
                        requests.delete(f"{API_BASE}/quizzes/{quiz_id}/questions")
                        
                    except requests.exceptions.RequestException as e:
                        st.error(f"❌ Failed to update quiz: {e}")
                        return
                        
                else:
                    # CREATING NEW QUIZ
                    base_name = ss.get("new_quiz_name") or ss.get("quiz_name", "Untitled Quiz")
                    if "quiz_creation_id" not in ss:
                        ss.quiz_creation_id = int(time.time() * 1000)  # milliseconds for uniqueness
                    unique_name = f"{base_name}_{ss.quiz_creation_id}"
                    
                    quiz_payload = {
                        "quiz_name": unique_name,
                        "number_question": len(ss.quiz_tuples),
                        "creator_id": ss.get("creator_id", 1),
                    }
                    
                    try:
                        # Create the quiz
                        r = requests.post(f"{API_BASE}/quizzes/", json=quiz_payload)
                        r.raise_for_status()
                        quiz_data = r.json()
                        new_quiz_id = quiz_data["id"]
                        
                    except requests.exceptions.RequestException as e:
                        st.error(f"❌ Failed to create quiz: {e}")
                        return
                
                try:

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
                        rq = requests.post(f"{API_BASE}/quizzes/{new_quiz_id}/questions", json=question_payload)
                        rq.raise_for_status()
                        questions_added += 1

                    # Success - clear state and reset
                    action = "updated" if quiz_id else "created"
                    st.success(f"✅ Quiz {action} successfully! ID: {new_quiz_id} ({questions_added} questions)")
                    ss.last_published_quiz = ss.quiz_tuples.copy()  # Track what was published
                    ss.quiz_tuples = []
                    ss.publishing = False
                    ss.publish_start_time = None
                    ss.new_quiz_name = None  # Clear the new quiz name
                    reset_editor()
                    ss.is_editing = False
                    ss.refresh_widgets = True
                    st.rerun()

                except requests.exceptions.RequestException as e:
                    ss.publishing = False
                    ss.publish_start_time = None
                    st.error(f"❌ Network error: {e}")
                except Exception as e:
                    ss.publishing = False
                    ss.publish_start_time = None
                    st.error(f"❌ Failed to publish quiz: {e}")

    # ADD / UPDATE
    with col_right:
        # Read current editor (scratchpad)
        qtext, (v0, v1, v2, v3), correct_idx = get_editor_values()

        # ADD
        if not ss.is_editing:
            if st.button("ADD"):
                # Append a copy so editor typing won't mutate saved list
                ss.quiz_tuples.append((qtext, tuple([v0, v1, v2, v3]), correct_idx))
                ss.last_published_quiz = None  # Reset published tracking when adding questions
                st.success("Question added!")
                reset_editor()
                ss.is_editing = False
                ss.refresh_widgets = True
                st.rerun()

        # UPDATE
        if ss.is_editing:
            if st.button("UPDATE"):
                if 0 <= ss.cursor < len(ss.quiz_tuples):
                    ss.quiz_tuples[ss.cursor] = (qtext, tuple([v0, v1, v2, v3]), correct_idx)
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
                if st.button(f"Fråga {i+1}: {qtext}", key=f"show_q_{i}"):
                    ss.editing = {"text": qtext, "choices": list(choices), "correct_index": correct_idx}
                    ss.cursor = i
                    ss.is_editing = True
                    ss.refresh_widgets = True
                    st.rerun()

            with col_edit:
                if st.button(" Edit", key=f"edit{i}"):
                    ss.editing = {"text": qtext, "choices": list(choices), "correct_index": correct_idx}
                    ss.cursor = i
                    ss.is_editing = True
                    ss.refresh_widgets = True
                    st.rerun()

            with col_delete:
                if st.button(" Delete", key=f"delete{i}"):
                    ss.quiz_tuples.pop(i)
                    st.success(f"Question {i + 1} deleted.")
                    reset_editor()
                    ss.is_editing = False
                    ss.refresh_widgets = True
                    st.rerun()


# Init + optional preload from backend
init_state()

# Load existing quiz data if editing
if quiz_id and "quiz_loaded" not in st.session_state:
    quiz_data = fetch_quiz_with_questions(quiz_id)
    if quiz_data:
        st.session_state.quiz_name = quiz_data.get("quiz_name", "Untitled Quiz")
        st.session_state.creator_id = quiz_data.get("creator_id", 1)
        questions = quiz_data.get("questions", [])
        st.session_state.quiz_tuples = [
            (q["question_text"], (q["choice_1"], q["choice_2"], q["choice_3"], q["choice_4"]), q["answer"]) for q in questions
        ]
        st.session_state.quiz_loaded = True

page_add_questions()
