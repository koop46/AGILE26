from __future__ import annotations
from pathlib import Path
from state import reset_editor
import requests
import streamlit as st
import os
from state import (
    init_state,
    load_into_editor,
    save_editor_into_questions,
    delete_current_question,
)


API_BASE = "http://localhost:8000"
quiz_id = st.session_state.get("selected_quiz_id")

ss = st.session_state
if "quiz_tuples" not in ss:
    ss.quiz_tuples = []


def fetch_quiz_with_questions(quiz_id: int):
    try:
        r = requests.get(f"{API_BASE}/quizzes/{quiz_id}")
        r.raise_for_status()
        return r.json()  # Innehåller quiz + frågor
    except Exception as e:
        st.error(f"Failed to fetch quiz {quiz_id}: {e}")
        return None


def api_add_question(quiz_id: int, question: dict):
    """Skicka en fråga till API:et och spara i DB"""
    try:
        r = requests.post(f"{API_BASE}/quizzes/{quiz_id}/questions", json=question)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        st.error(f"Failed to add question: {e}")
        return None


# Setup
st.set_page_config(page_title="Create Quiz – Add Questions", layout="wide")


def load_css():
    here = Path(__file__).parent
    for p in (here / "styles" / "create_quiz.css", here.parent / "styles" / "create_quiz.css"):
        if p.is_file():
            st.markdown(f"<style>{p.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)
            return


# Page
def page_add_questions():
    load_css()
    st.markdown('<div id="create-quiz">', unsafe_allow_html=True)

    ss = st.session_state
    ss.setdefault("cursor", 0)

    with st.sidebar:
        st.header("Questions")
        if ss.quiz_tuples:
            for i, (qtext, choices, correct_idx) in enumerate(ss.quiz_tuples):
                label = f"{i+1} - {qtext[:26]}{'…' if len(qtext) > 26 else ''}"
                st.write(label)
                for j, c in enumerate(choices):
                    prefix = " " if j == correct_idx else "- "
                    st.write(f"{prefix}{c}")
        else:
            st.info("No questions added yet.")

    left, main, right = st.columns([1, 3, 1])

    with main:
        if not ss.get("initialized_editor", False):
            load_into_editor(ss.questions[0] if ss.get("questions") else None)
            ss.initialized_editor = True

        e = ss.editing

        st.markdown('<div class="quiz-title">', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="question-header">WRITE YOUR QUESTION</div>', unsafe_allow_html=True)
        qtext = st.text_area(
            "",
            value=e["text"],
            height=120,
            label_visibility="collapsed",
            key="editing_text",
            placeholder="Type your question here…",
        )

        correct_idx = st.radio(
            "",
            options=[0, 1, 2, 3],
            index=e["correct_index"],
            horizontal=True,
            label_visibility="collapsed",
            key="editing_correct_index",
        )

        r1c1, r1c2 = st.columns(2, gap="large")
        with r1c1:
            v0 = st.text_input("", value=e["choices"][0], key="choice0", label_visibility="collapsed", placeholder="Choice 1")
        with r1c2:
            v1 = st.text_input("", value=e["choices"][1], key="choice1", label_visibility="collapsed", placeholder="Choice 2")

        r2c1, r2c2 = st.columns(2, gap="large")
        with r2c1:
            v2 = st.text_input("", value=e["choices"][2], key="choice2", label_visibility="collapsed", placeholder="Choice 3")
        with r2c2:
            v3 = st.text_input("", value=e["choices"][3], key="choice3", label_visibility="collapsed", placeholder="Choice 4")

    col_left, col_right = st.columns([1.2, 0.1])

    with col_left:
        st.markdown('<div class="btn-delete">', unsafe_allow_html=True)
        if st.button("DELETE", key="delete_bottom"):
            delete_current_question()
        st.markdown("</div>", unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="btn-add">', unsafe_allow_html=True)
        if st.button("ADD"):
            current_tuple = (
                qtext,
                (v0, v1, v2, v3),
                correct_idx,
            )
            ss.quiz_tuples.append(current_tuple)  # always add new tuple
            st.success(" Question added to tuple list!")
            reset_editor()
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="btn-save">', unsafe_allow_html=True)
        if st.button("SAVE"):
            current_tuple = (
                qtext,
                (v0, v1, v2, v3),
                correct_idx,
            )
            if ss.quiz_tuples:
                ss.quiz_tuples[ss.cursor] = current_tuple
                st.success(" Question updated in tuple list!")
            else:
                ss.quiz_tuples.append(current_tuple)
                st.success(" First question saved!")
            reset_editor()
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    total = len(ss.get("quiz_tuples", []))
    st.caption(f"Total questions: {total}")

'''
if st.session_state.questions:
    for i, q in enumerate(st.sessionstate.questions):
        st.subheader(f"Fråga {i + 1}: {q['question']}")
        for i, opt in enumerate(q["options"]):
            marker = "✅" if i == q["correct"] else "-"
            st.write(f"{marker} {opt}")
        else:
                st.write(f"- {opt}")
        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"✏️ Redigera", key=f"edit{i}"):
                st.session_state.edit_index = i
                st.experimentalrerun()
        with col2:
            if st.button(f"🗑️ Ta bort", key=f"delete{i}"):
                st.session_state.questions.pop(i)
                st.success(f"Fråga {i + 1} har tagits bort.")
                st.experimental_rerun()

    # Spara quiz-knapp
    st.header("Spara quiz")
    if st.button("💾 Spara quiz"):
        st.success("Quizet har sparats! (simulerat)")
        
'''

# Init
init_state()
page_add_questions()
