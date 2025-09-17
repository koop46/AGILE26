import streamlit as st
from models import QuizDraft
from state import load_into_editor, save_editor_into_questions, delete_current_question



def page_add_questions():
    st.title("Create Quiz – Add Questions")
    st.caption("Add questions with multiple choices (exactly one correct).")

    ss = st.session_state
    ss.setdefault("cursor", 0)  # safety belt in case init_state wasn't called

    #  SIDEBAR
    with st.sidebar:
        st.header("Quiz Title")
        st.text_input("Enter the title of your quiz:", key="quiz_title")

        st.header("Questions")
        if ss.questions:
            for i, q in enumerate(ss.questions):
                label = f"Edit Q{i+1}: {q.text[:30]}{'…' if len(q.text) > 30 else ''}"
                if st.button(label, key=f"edit_{i}"):
                    ss.cursor = i
                    load_into_editor(ss.questions[ss.cursor])
        else:
            st.info("No questions added yet.")

        st.divider()
        if st.button("Save quiz"):
            ok = True
            if ss.get("dirty"):
                ok = save_editor_into_questions(new_slot=False)   # save current edits
            if ok and ss.questions and ss.quiz_title.strip():
                draft = QuizDraft(ss.quiz_title.strip(), ss.questions)
                save_quiz_draft(draft)
                st.success("Quiz draft saved!")
            else:
                if not ss.quiz_title.strip():
                    st.error("Quiz title cannot be empty.")
                if not ss.questions:
                    st.error("Add at least one question before saving.")

    # EDITOR INIT 
    if not ss.get("initialized_editor", False):
        load_into_editor(ss.questions[0] if ss.questions else None)
        ss.initialized_editor = True

    e = ss.editing  

    #  MAIN EDITOR
    new_text = st.text_area("Question", value=e["text"], key="editing_text", height=100)
    if new_text != e["text"]:
        ss.editing["text"] = new_text
        ss.dirty = True

    st.write("**Choices (pick one correct)**")
    cols = st.columns([1, 5])

    # to choose the correct answer
    correct_idx = e["correct_index"]
    with cols[0]:
        correct_idx = st.radio(
            "Correct",
            options=list(range(len(e["choices"]))),  
            index=e["correct_index"],
            key="editing_correct_index",
            label_visibility="collapsed",
            format_func=lambda i: f"#{i+1}",
        )

    # choice inputs (strings)
    for idx in range(len(e["choices"])):
        with cols[1]:
            val = st.text_input(
                f"Choice {idx+1}",
                value=e["choices"][idx],
                key=f"editing_choice_{idx}",
            )
            if val != e["choices"][idx]:
                ss.editing["choices"][idx] = val
                ss.dirty = True

    if correct_idx != e["correct_index"]:
        ss.editing["correct_index"] = correct_idx
        ss.dirty = True

    #  ACTION BUTTONS 
    col1, col2 = st.columns(2)

    ss.dirty = True

    with col1:
       if st.button("Previous") and ss.questions:
            ss.cursor = max(0, ss.cursor - 1)
            load_into_editor(ss.questions[ss.cursor])
    

    with col2:
        if st.button("Next"):
            if save_editor_into_questions(new_slot=not ss.questions):
                if ss.cursor < len(ss.questions) - 1:
                    ss.cursor += 1
                    load_into_editor(ss.questions[ss.cursor])
                

    d1, d2 = st.columns(2)
    with d1:
        if st.button("Delete this question"):
            delete_current_question()
    with d2:
        if st.button("Save"):
            save_editor_into_questions(new_slot=False)

    total = len(ss.questions)
    st.caption(f"Question {ss.cursor + 1 if total else 0} of {total}")



custom_css = """
 <style>
    div.stButton > button{
        background-color: #4CAF50;
    }
    
    div.stButton:hover > button{
        background-color: #4C3650;
        transform: scale(1.5);
    }
    </style>
 
 """
 
 
st.markdown(custom_css, unsafe_allow_html=True)