import streamlit as st

# Import CSS styles
def load_css():
    with open("pages/styles/0_Home_Page.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()



col_1, col_2, col_3 = st.columns(3)

with col_2:
    st.markdown('<div id="col-2"></div>', unsafe_allow_html=True)
    st.title("QuizApp")

col1, col2, col3 = st.columns([2,1,4])

with col1:
    # Button with action
    if st.button("Create a Quiz", key="main_quiz_button", type="primary"):
        st.switch_page("app.py")

with col3:
    #items = get_quiz_list_from_database()  # Database function
    items = ("This is my first Quiz", "Lecture in Agile programing", "Wow this app is so cool")
    
    for item in items:
        with st.container():
            col_a, col_b = st.columns([5, 1])
            with col_a:
                st.write(f"{item}")
            with col_b:
                if st.button("Take", key=f"take_{item}"):
                    st.write("taking Quiz")
                    # Add action for taking the quiz 


# Centered button with adjustable vertical placement








load_css()


