import streamlit as st

# Import CSS styles
def load_css():
    with open("pages/0_Home_Page.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()


col_1, col_2, col_3 = st.columns(3)

with col_2:
    st.markdown('<div id="col-2"></div>', unsafe_allow_html=True)
    st.title("QuizApp")

col1, col2, col3 = st.columns(3)

with col2:
    st.button("Create a Quiz")

with col3:
    items = ["Quiz 1", "Quiz 2", "Quiz 3"]
    st.markdown("\n".join(f"- {x}" for x in items)) 







load_css()


