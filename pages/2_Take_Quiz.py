import streamlit as st
import requests
#from rel.crud_operations import ResourceClient
#from app import API_BASE

API_BASE = "http://localhost:8000"


quiz_id = st.session_state.get("selected_quiz_id")

if not quiz_id:
    st.error(" No quiz selected. Go back to the homepage and choose a quiz first.")
    st.stop()

# Initialize session variables
if "current_question_index" not in st.session_state:
    st.session_state.current_question_index = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "user_answers" not in st.session_state:
    st.session_state.user_answers = []
if "student_name" not in st.session_state:
    st.session_state.student_name = ""  
if "quiz_started" not in st.session_state:
    st.session_state.quiz_started = False 
    

# Fetch quiz with questions
@st.cache_data(show_spinner=False)
def fetch_quiz(quiz_id):
    r = requests.get(f"{API_BASE}/quizzes/{quiz_id}")
    r.raise_for_status()
    return r.json()


#  Get quiz data 
quiz_data = fetch_quiz(quiz_id)
if not quiz_data:
    st.stop()

questions = quiz_data.get("questions", [])
if not questions:
    st.warning("This quiz has no questions.")
    st.stop()

# quiz title
st.markdown(f"##  {quiz_data.get('quiz_name', 'Untitled Quiz')}")

#  name before starting
if not st.session_state.quiz_started:
    st.write(" Enter your name:")
    st.session_state.student_name = st.text_input("Your name:", key="student_name_input")

    if st.button("Start Quiz"):
        if not st.session_state.student_name.strip():
            st.warning(" Enter your name to start.")
        else:
            st.session_state.quiz_started = True
            st.rerun()

    st.stop()  


st.markdown(f"{st.session_state.student_name}")
 
index = st.session_state.current_question_index

#  End of quiz
if index >= len(questions):
    st.write(f"Your final score: **{st.session_state.score} / {len(questions)}**")
    if st.button(" Go back to homepage"):
        st.switch_page("pages/0_Home_Page.py")
    st.stop()

# Current question
current_q = questions[index]

choices = [
    current_q.get("choice_1", ""),
    current_q.get("choice_2", ""),
    current_q.get("choice_3", ""),
    current_q.get("choice_4", ""),
]

st.markdown(f"### Question {index + 1} of {len(questions)}")
st.write(current_q["question_text"])

# Load previous answer if navigating back
prev_answer = st.session_state.user_answers[index] if index < len(st.session_state.user_answers) else None

selected_idx = st.radio(
    "Select your answer:",
    options=[0, 1, 2, 3],
    format_func=lambda i: choices[i],
    index=prev_answer if prev_answer is not None else 0,
    key=f"choice_{index}"
)


col_prev, col_next = st.columns([1, 1])

#  Previous Button
with col_prev:
    if st.button("Previous"):
        if st.session_state.current_question_index > 0:
            st.session_state.current_question_index -= 1
            st.rerun()

#  Next / Submit Button
index = st.session_state.current_question_index
is_last = (index == len(questions) - 1)
button_label = "Submit Quiz" if is_last else " Next"

with col_next:
    if st.button(button_label):
        if index < len(st.session_state.user_answers):
            st.session_state.user_answers[index] = selected_idx
        else:
            st.session_state.user_answers.append(selected_idx)

        # Recalculate score dynamically
        st.session_state.score = sum(
            1
            for i, q in enumerate(questions[:len(st.session_state.user_answers)])
            if st.session_state.user_answers[i] == q.get("answer", 0)
        )

        if is_last:
            results_payload = {
                "quiz_name": quiz_data.get("quiz_name", "Untitled Quiz"),
                "student_name": st.session_state.student_name,
                "score": st.session_state.score,
                "total": len(questions),
                "details": [
                    {
                        "index": i,
                        "question_text": q.get("question_text", ""),
                        "chosen": q.get(f"choice_{st.session_state.user_answers[i] + 1}", ""),
                        "correct": q.get(f"choice_{q.get('answer', 0) + 1}", ""),
                        "is_correct": st.session_state.user_answers[i] == q.get("answer", 0)
                    }
                    for i, q in enumerate(questions)
                ]
            }

            # Store results in session state
            st.session_state["results_payload"] = results_payload

            #
            st.switch_page("pages/3_Results_Dashboards.py")

        else:
            # Next question
            st.session_state.current_question_index += 1
            st.rerun()




####### La till detta tillfälligt ##########
def page_take_quiz():
    st.title("🧠 Take Quiz")

    # --- Tillbaka till app-sidan ---
    if st.button("⬅️ Tillbaka till app-sidan"):
        st.session_state["current_page"] = "home"
        st.switch_page("app.py")

    # --- Resten av din quiz-logik här ---
    st.write("Här kommer quizet att visas...")

