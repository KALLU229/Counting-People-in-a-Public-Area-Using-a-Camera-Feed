import streamlit as st
from db import validate_user

def login_page():
    st.title("Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = validate_user(email, password)
        if user:
            st.session_state.logged_in = True
            st.session_state.role = user["role"]
            st.session_state.email = user["email"]
            st.experimental_rerun()
        else:
            st.error("Invalid credentials")
