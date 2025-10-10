from __future__ import annotations
from rel.crud_operations import ResourceClient
from app import API_BASE
import streamlit as st

quiz_table = ResourceClient(base_url=API_BASE, endpoint_path="/quizzes/")

def main():
    st.title("Results")
    payload = st.session_state.get("results_payload")

    if not payload:
        st.info("No results found in the session.")
        if st.session_state.get("selected_quiz_id"):
            if st.button("Back to quiz"):
                try:
                    st.switch_page("pages/2_Take_Quiz.py")
                except Exception:
                    return
        return

    #  Quiz Info
    quiz_name = payload.get("quiz_name")
    student_name = payload.get("student_name") or "Anonymous"
    score = payload.get("score", 0)
    total = payload.get("total", 0)
    details = payload.get("details", [])

    #  Header Section 
    st.subheader(quiz_name)
    st.write(f"**Student:** {student_name}")
    st.success(f"**Score:** {score}/{total}")

    st.markdown("---")
    st.markdown("###  Answer Summary")

    #  Display all questions
    for d in details:
        is_correct = d.get("is_correct", False)
        icon = "✅" if is_correct else "❌"
        question_num = d.get("index", 0) + 1
        q_text = d.get("question_text", "—")
        chosen = d.get("chosen", "—")
        correct = d.get("correct", "—")

        st.markdown(
            f"""
            <div style="padding: 10px 14px; margin-bottom: 10px; border-radius: 6px;">
                <p style="margin:0; font-size:16px;">
                    {icon} <b>Question {question_num}:</b> {q_text}
                </p>
                <ul style="margin: 4px 0 0 25px; line-height: 1.6;">
                    <li><b>Your answer:</b> {chosen}</li>
                    <li><b>Correct answer:</b> {correct}</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    #  Navigation Buttons 
    st.markdown("---")
    col1, col2 = st.columns(2)

    # Retake Quiz button
    with col1:
        if st.button(" Retake Quiz"):
            # Clear old widget states
            for key in list(st.session_state.keys()):
                if key.startswith("choice_"):
                    del st.session_state[key]

            
            st.session_state.current_question_index = 0
            st.session_state.score = 0
            st.session_state.user_answers = []
            st.session_state.quiz_started = True  

           
            st.switch_page("pages/2_Take_Quiz.py")

    # Go back to preview
    with col2:
        if st.button(" To Quiz Preview"):
            st.switch_page("pages/5_Quiz_Preview.py")


if __name__ == "__main__":
    main()
