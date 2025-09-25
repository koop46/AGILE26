from __future__ import annotations
from pathlib import Path
import streamlit as st
from state import (
    init_state,
    load_into_editor,
    save_editor_into_questions,
    delete_current_question,
)

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

    with st.sidebar:
        st.header("Questions")
        if ss.get("questions"):
            for i, q in enumerate(ss.questions):
                label = f"{i+1} - {q.text[:26]}{'…' if len(q.text) > 26 else ''}"
                if st.button(label, key=f"nav_{i}"):
                    ss.cursor = i
                    load_into_editor(ss.questions[ss.cursor])
        else:
            st.info("No questions added yet.")

    left, main, right = st.columns([1, 3, 1])

    with main:
        if not ss.get("initialized_editor", False):
            load_into_editor(ss.questions[0] if ss.get("questions") else None)
            ss.initialized_editor = True

        e = ss.editing

        st.markdown('<div class="quiz-title-label">QUIZ TITLE</div>', unsafe_allow_html=True)
        st.markdown('<div class="quiz-title">', unsafe_allow_html=True)
        st.text_input("", key="quiz_title", label_visibility="collapsed", placeholder="Type your quiz title…")
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
        if qtext != e["text"]:
            ss.editing["text"] = qtext
            ss.dirty = True

        correct_idx = st.radio(
            "",
            options=[0, 1, 2, 3],
            index=e["correct_index"],
            horizontal=True,
            label_visibility="collapsed",
            key="editing_correct_index",
        )
        if correct_idx != e["correct_index"]:
            ss.editing["correct_index"] = correct_idx
            ss.dirty = True

        r1c1, r1c2 = st.columns(2, gap="large")
        with r1c1:
            st.markdown(f'<div class="choice-box {"correct" if correct_idx == 0 else ""}">', unsafe_allow_html=True)
            v0 = st.text_input("", value=e["choices"][0], key="choice0", label_visibility="collapsed", placeholder="Choice 1")
            st.markdown("</div>", unsafe_allow_html=True)
        with r1c2:
            st.markdown(f'<div class="choice-box {"correct" if correct_idx == 1 else ""}">', unsafe_allow_html=True)
            v1 = st.text_input("", value=e["choices"][1], key="choice1", label_visibility="collapsed", placeholder="Choice 2")
            st.markdown("</div>", unsafe_allow_html=True)

        r2c1, r2c2 = st.columns(2, gap="large")
        with r2c1:
            st.markdown(f'<div class="choice-box {"correct" if correct_idx == 2 else ""}">', unsafe_allow_html=True)
            v2 = st.text_input("", value=e["choices"][2], key="choice2", label_visibility="collapsed", placeholder="Choice 3")
            st.markdown("</div>", unsafe_allow_html=True)
        with r2c2:
            st.markdown(f'<div class="choice-box {"correct" if correct_idx == 3 else ""}">', unsafe_allow_html=True)
            v3 = st.text_input("", value=e["choices"][3], key="choice3", label_visibility="collapsed", placeholder="Choice 4")
            st.markdown("</div>", unsafe_allow_html=True)

        if [v0, v1, v2, v3] != e["choices"]:
            ss.editing["choices"] = [v0, v1, v2, v3]
            ss.dirty = True

    col_left, col_right = st.columns([1.2, 0.1])

    with col_left:
        st.markdown('<div class="btn-prev">', unsafe_allow_html=True)
        if st.button("PREVIOUS") and ss.get("questions"):
            ss.cursor = max(0, ss.cursor - 1)
            load_into_editor(ss.questions[ss.cursor])
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="btn-delete">', unsafe_allow_html=True)
        if st.button("DELETE", key="delete_bottom"):
            delete_current_question()
        st.markdown("</div>", unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="btn-add">', unsafe_allow_html=True)
        if st.button("ADD"):
            if save_editor_into_questions(new_slot=not ss.get("questions"), show_errors=False):
                load_into_editor(None)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="btn-save">', unsafe_allow_html=True)
        if st.button("SAVE"):
            save_editor_into_questions(new_slot=False, show_errors=True)
        st.markdown("</div>", unsafe_allow_html=True)

    total = len(ss.get("questions", []))
    st.caption(f"Question {ss.cursor + 1 if total else 0} of {total}")

    st.markdown("</div>", unsafe_allow_html=True)


init_state()
page_add_questions()
