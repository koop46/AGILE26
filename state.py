import streamlit as st
from models import Choice, Question

def init_state():
    ss= st.session_state
    ss.setdefault("quiz_title", "")
    ss.setdefault("questions", [])
    ss.setdefault("cursor", 0)
    ss.setdefault(
        "editing",
        {"text": "", "choices": ["", "", "", ""], "correct_index": 0  })
    ss.setdefault("initialized_editor", False)

# Set up the question editor.
# If q is None, initialize with empty fields for a new question.
# Otherwise, pre-fill with the data from the given Question object.
def load_into_editor(q: Question):
    if q is None:
        st.session_state.editing = {
            "text": "",
            "choices": ["", "", "", ""],
            "correct_index": 0,
        }
    else:
        st.session_state.editing = {
            "text": q.text,
            "choices": [c.text for c in q.choices] + [""] * max(0, 4 - len(q.choices)),
            "correct_index": q.correct_index,  
        }

def save_editor_into_questions(new_slot: bool = False) -> bool:
    ss = st.session_state
    editor = ss.editing

    # Read input from the editor
    text = editor["text"].strip()
    choices_texts = [c.strip() for c in editor["choices"] if c.strip()]
    correct_index = editor["correct_index"]

    if not text:
        return False
    if len(choices_texts) < 2:
        return False

    # Build a Question
    q = Question(
        text=text,
        choices=[Choice(text=c) for c in choices_texts],
        correct_index=correct_index,
    )

    # Save into session_state
    if new_slot or not ss.get("questions"):
        ss.questions.append(q)
        ss.cursor = len(ss.questions) - 1
    else:
        ss.questions[ss.cursor] = q

    return True




def delete_current_question() -> None:
    ss = st.session_state
    if not ss.questions:
        return
    del ss.questions[ss.cursor]
    if ss.questions:
        ss.cursor = max(0, min(ss.cursor, len(ss.questions) - 1))
        load_into_editor(ss.questions[ss.cursor])
    else:
        ss.cursor = 0
        load_into_editor(None)

def reset_editor():
    st.session_state.editing = {
        "text": "",
        "choices": ["", "", "", ""],
        "correct_index": 0,
    }


