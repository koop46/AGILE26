from __future__ import annotations
from pathlib import Path
from state import reset_editor
import requests
import streamlit as st
import os
from state import (
    init_state,
    load_into_editor,
    # save_editor_into_questions,
    # delete_current_question,
)

API_BASE = "http://localhost:8000"
quiz_id = st.session_state.get("selected_quiz_id")

ss = st.session_state
if "quiz_tuples" not in ss:
    ss.quiz_tuples = []
if "is_editing" not in ss:
    ss.is_editing = False   


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


def page_add_questions():
    load_css()
    st.markdown('<div id="create-quiz">', unsafe_allow_html=True)

    ss = st.session_state
    ss.setdefault("cursor", 0)

    left, main, right = st.columns([1, 3, 1])

    with main:
        if not ss.get("initialized_editor", False):
            load_into_editor(ss.questions[0] if ss.get("questions") else None)
            ss.initialized_editor = True

        e = ss.editing

        #  editor UI
        st.markdown('<div class="question-header">WRITE YOUR QUESTION</div>', unsafe_allow_html=True)
        qtext = st.text_area("", value=e["text"], height=120, key="editing_text", placeholder="Type your question here…")

        correct_idx = st.radio(
            "", options=[0, 1, 2, 3],
            index=e["correct_index"], horizontal=True,
            key="editing_correct_index"
        )

        r1c1, r1c2 = st.columns(2, gap="large")
        with r1c1:
            v0 = st.text_input("", value=e["choices"][0], key="choice0", placeholder="Choice 1")
        with r1c2:
            v1 = st.text_input("", value=e["choices"][1], key="choice1", placeholder="Choice 2")

        r2c1, r2c2 = st.columns(2, gap="large")
        with r2c1:
            v2 = st.text_input("", value=e["choices"][2], key="choice2", placeholder="Choice 3")
        with r2c2:
            v3 = st.text_input("", value=e["choices"][3], key="choice3", placeholder="Choice 4")

    col_left, col_right = st.columns([1.2, 0.1])

    with col_right:
        # ADD-knapp 
        if not ss.is_editing:
            if st.button("ADD"):
                current_tuple = (qtext, (v0, v1, v2, v3), correct_idx)
                ss.quiz_tuples.append(current_tuple)
                st.success("Question added!")
                reset_editor()
                st.rerun()

        # UPDATE-knapp 
        if ss.is_editing:
            if st.button("UPDATE"):
                current_tuple = (qtext, (v0, v1, v2, v3), correct_idx)
                if 0 <= ss.cursor < len(ss.quiz_tuples):
                    ss.quiz_tuples[ss.cursor] = current_tuple
                    st.success(" Question updated!")
                ss.is_editing = False
                reset_editor()
                st.rerun()

        # SAVE-knapp (alltid tillgänglig) 
        if st.button("SAVE"):
            current_tuple = (qtext, (v0, v1, v2, v3), correct_idx)
            if ss.quiz_tuples and 0 <= ss.cursor < len(ss.quiz_tuples):
                ss.quiz_tuples[ss.cursor] = current_tuple
                st.success(" Question saved locally!")
            else:
                ss.quiz_tuples.append(current_tuple)
                st.success(" First question saved!")
            reset_editor()
            st.rerun()

    total = len(ss.get("quiz_tuples", []))
    st.caption(f"Total questions: {total}")

    # SPARADE FRÅGOR 
    if ss.quiz_tuples:
        st.divider()
        st.header("Questions: ")

        for i, (qtext, choices, correct_idx) in enumerate(ss.quiz_tuples):
            col_q, col_edit, col_delete = st.columns([3, 1, 1])

            with col_q:
                if st.button(f"Fråga {i+1}: {qtext}", key=f"show_q_{i}"):
                    ss.editing = {"text": qtext, "choices": list(choices), "correct_index": correct_idx}
                    ss.cursor = i
                    ss.is_editing = True
                    st.rerun()

            with col_edit:
                if st.button(" Edit", key=f"edit{i}"):
                    ss.editing = {"text": qtext, "choices": list(choices), "correct_index": correct_idx}
                    ss.cursor = i
                    ss.is_editing = True
                    st.rerun()

            with col_delete:
                if st.button(" Delete", key=f"delete{i}"):
                    ss.quiz_tuples.pop(i)
                    st.success(f"Question {i + 1} is deleted.")
                    st.rerun()


# Init
init_state()
page_add_questions()
