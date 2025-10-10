from rel.crud_operations import ResourceClient
from app import API_BASE
import streamlit as st ##### <- la till denna ######



quiz_table = ResourceClient(base_url=API_BASE, endpoint_path="/quizzes/")

#quiz_table.create(json_payload)
# quiz_table.get_one(id)
# quiz_table.get_all()
# quiz_table.update(id, json_payload)


####### La till detta tillfälligt ##########
def page_take_quiz():
    st.title("🧠 Take Quiz")

    # --- Tillbaka till app-sidan ---
    if st.button("⬅️ Tillbaka till app-sidan"):
        st.session_state["current_page"] = "home"
        st.switch_page("app.py")

    # --- Resten av din quiz-logik här ---
    st.write("Här kommer quizet att visas...")



if __name__ == "__main__":
    page_take_quiz()

###################################
