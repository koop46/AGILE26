import streamlit as st
from ui.add_questions import page_add_questions
from state import init_state

# This file makes 'ui' import page_add_questions

st.set_page_config(page_title="BrainTap – Add Questions",  layout="wide")

def main():
    init_state()
    page_add_questions()

if __name__ == "__main__":
    main()
