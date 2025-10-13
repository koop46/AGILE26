import streamlit as st
import requests

API_BASE = "http://localhost:8000"

# Retrieve selected quiz ID from session
quiz_id = st.session_state.get("selected_quiz_id")
if not quiz_id:
    st.error("No quiz selected. Go back to the homepage and choose a quiz first.")
    st.stop()
    
def clean_quiz_name(name: str) -> str:
    if "_" in name and name.split("_")[-1].isdigit():
        return "_".join(name.split("_")[:-1])
    return name


# Initialize session variables
ss = st.session_state
if "current_question_index" not in ss:
    ss.current_question_index = 0
if "score" not in ss:
    ss.score = 0
if "user_answers" not in ss:
    ss.user_answers = []
if "student_name" not in ss:
    ss.student_name = ""
if "quiz_started" not in ss:
    ss.quiz_started = False

# Fetch quiz once
@st.cache_data(show_spinner=False)
def fetch_quiz(qid: int):
    r = requests.get(f"{API_BASE}/quizzes/{qid}")
    r.raise_for_status()
    return r.json()

quiz_data = fetch_quiz(quiz_id)
questions = quiz_data.get("questions", [])
if not questions:
    st.warning("This quiz has no questions.")
    st.stop()

# Title
quiz_name = clean_quiz_name(quiz_data.get("quiz_name", "Untitled Quiz"))
st.markdown(f"## {quiz_name}")


#name 
if not ss.quiz_started:
    st.write("Enter your name:")
    ss.student_name = st.text_input("Your name:", key="student_name_input")
    if st.button("Start Quiz"):
        if not ss.student_name.strip():
            st.warning("Please enter your name to start.")
        else:
            ss.quiz_started = True
            st.rerun()
    st.stop()

st.markdown(f"**Good luck, {ss.student_name}!** ")

# Helper: record/update answer + scoring
def record_answer(idx_question: int, selected_idx: int):
    if idx_question < len(ss.user_answers):
        ss.user_answers[idx_question] = selected_idx
    else:
        ss.user_answers.append(selected_idx)

    # recompute score
    ss.score = sum(
        1
        for i, q in enumerate(questions[:len(ss.user_answers)])
        if ss.user_answers[i] == q.get("answer", 0)
    )

# finish quiz & go to results dashboard
def finish_quiz():
    results_payload = {
        "quiz_name": quiz_data.get("quiz_name", "Untitled Quiz"),
        "student_name": ss.student_name,
        "score": ss.score,
        "total": len(questions),
        "details": [
            {
                "index": i,
                "question_text": q.get("question_text", ""),
                "chosen": q.get(f"choice_{ss.user_answers[i] + 1}", "")
                if i < len(ss.user_answers) else "",
                "correct": q.get(f"choice_{q.get('answer', 0) + 1}", ""),
                "is_correct": (ss.user_answers[i] == q.get("answer", 0))
                if i < len(ss.user_answers) else False,
            }
            for i, q in enumerate(questions)
        ],
    }
    ss["results_payload"] = results_payload
    st.switch_page("pages/3_Results_Dashboards.py")

# Current index + end state
idx = ss.current_question_index
if idx >= len(questions):
    st.success(f"You've completed the quiz! Final score: **{ss.score}/{len(questions)}**")
    if st.button("Go back to homepage"):
        st.switch_page("pages/0_Home_Page.py")
    st.stop()

#Current question data
q = questions[idx]
choices = [q.get("choice_1", ""), q.get("choice_2", ""), q.get("choice_3", ""), q.get("choice_4", "")]
prev_answer = ss.user_answers[idx] if idx < len(ss.user_answers) else None
is_last = (idx == len(questions) - 1)

# --- Question text ---
st.markdown(
    f"""
    <div style="
        width:100%;
        text-align:center;
        background:#f6f8fb;
        border-radius:14px;
        padding:16px 10px;
        margin:10px 0 18px 0;
        font-size:24px;
        font-weight:700;
        color:#111827;">
        {q.get("question_text", "")}
    </div>
    """,
    unsafe_allow_html=True,
)

# --- CSS for multi choices
st.markdown("""
<style>
.big-choice button {
    width: 100%;
    text-align: center;
    background: #ffffff;
    border: 2px solid #e5e7eb;
    border-radius: 14px;
    padding: 16px 18px;
    margin: 10px 0;
    font-size: 20px;
    font-weight: 500;
    color: #111827;
    transition: all 0.15s ease;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
.big-choice button:hover { background: #f8fafc; border-color: #c7d2fe; }
.big-choice button.selected { background: #eef2ff; border-color: #6366f1; color: #1e3a8a; }
</style>
""", unsafe_allow_html=True)


cols = st.columns(2)
clicked_choice = None

for i, text in enumerate(choices):
    col = cols[i % 2]
    with col:
        selected = (prev_answer == i)
        with st.container():
            st.markdown('<div class="big-choice">', unsafe_allow_html=True)
            clicked = st.button(text, key=f"choice_{idx}_{i}", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        if clicked:
            clicked_choice = i

if clicked_choice is not None:
    record_answer(idx, clicked_choice)
    if is_last:
        finish_quiz()
    else:
        ss.current_question_index += 1
        st.rerun()

#  Navigation buttons
nav_prev, nav_next = st.columns([1, 1])
with nav_prev:
    if st.button("Previous"):
        if ss.current_question_index > 0:
            ss.current_question_index -= 1
            st.rerun()

#with nav_next:
#    label = "Submit" if is_last else " Next"
#    if st.button(label):
#        if prev_answer is None:
#            st.warning("Please choose an option before continuing.")
#        else:
#            record_answer(idx, prev_answer)
            if is_last:
                finish_quiz()
            else:
                ss.current_question_index += 1
                st.rerun()

# Move "Question x of y" to bottom right
bottom_left, bottom_right = st.columns([3, 1])
with bottom_right:
    st.markdown(
        f"""
        <div style="
            text-align:right;
            font-size:16px;
            color:#6b7280;
            margin-top:10px;
            padding-right:8px;">
            Question {idx + 1} of {len(questions)}
        </div>
        """,
        unsafe_allow_html=True
    )
