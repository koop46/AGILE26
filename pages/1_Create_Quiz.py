from __future__ import annotations
from pathlib import Path
import requests
import streamlit as st
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


def api_add_question(quiz_id: int, question: dict):
    try:
        r = requests.post(f"{API_BASE}/quizzes/{quiz_id}/questions", json=question)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        st.error(f"Failed to add question: {e}")
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
        st.text_area("", key="editing_text", height=120, placeholder="Type your question here…")
        st.radio("", options=[0, 1, 2, 3], key="editing_correct_index", horizontal=True)

        r1c1, r1c2 = st.columns(2, gap="large")
        with r1c1:
            st.text_input("", key="choice0", placeholder="Choice 1")
        with r1c2:
            st.text_input("", key="choice1", placeholder="Choice 2")

        r2c1, r2c2 = st.columns(2, gap="large")
        with r2c1:
            st.text_input("", key="choice2", placeholder="Choice 3")
        with r2c2:
            st.text_input("", key="choice3", placeholder="Choice 4")

    col_left, col_right = st.columns([1.2, 0.1])

    # PUBLISH
    with col_left:
        if st.button("PUBLISH QUIZ"):
            if len(ss.quiz_tuples) < 1:
                st.error("You must add at least 1 question before publishing.")
            else:
                quiz_payload = {
                    "quiz_name": ss.get("quiz_name", "Untitled Quiz"),
                    "number_question": len(ss.quiz_tuples),
                    "creator_id": ss.get("creator_id", 1),
                }
                try:
                    r = requests.post(f"{API_BASE}/quizzes/", json=quiz_payload)
                    r.raise_for_status()
                    quiz_data = r.json()
                    new_quiz_id = quiz_data["id"]

                    for (qtext, choices, correct_idx) in ss.quiz_tuples:
                        question_payload = {
                            "text": qtext,
                            "choices": list(choices),
                            "correct_index": correct_idx,
                        }
                        rq = requests.post(f"{API_BASE}/quizzes/{new_quiz_id}/questions", json=question_payload)
                        rq.raise_for_status()

                    st.success(f"✅ Quiz published successfully! ID: {new_quiz_id}")
                    ss.quiz_tuples = []

                    reset_editor()
                    ss.is_editing = False
                    ss.refresh_widgets = True
                    st.rerun()

                except Exception as e:
                    st.error(f"Failed to publish quiz: {e}")

    # ADD / UPDATE
    with col_right:
        # Read current editor (scratchpad)
        qtext, (v0, v1, v2, v3), correct_idx = get_editor_values()

        # ADD
        if not ss.is_editing:
            if st.button("ADD"):
                # Append a copy so editor typing won’t mutate saved list
                ss.quiz_tuples.append((qtext, tuple([v0, v1, v2, v3]), correct_idx))
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
page_add_questions()
if quiz_id:
    quiz_data = fetch_quiz_with_questions(quiz_id)
    if quiz_data:
        st.session_state.quiz_name = quiz_data.get("quiz_name", "Untitled Quiz")
        st.session_state.creator_id = quiz_data.get("creator_id", 1)
        questions = quiz_data.get("questions", [])
        st.session_state.quiz_tuples = [
            (q["question_text"], q["answers"], q["correct_idx"]) for q in questions
        ]
