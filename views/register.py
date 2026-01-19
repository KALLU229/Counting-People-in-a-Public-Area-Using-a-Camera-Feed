import streamlit as st
from db import add_user

SUPER_ADMIN_PASSWORD = "kalludon"

def register_page():
    st.title("Register")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    role = st.radio("Register as", ["User", "Admin"])

    super_code = None
    if role == "Admin":
        super_code = st.text_input("Super Password", type="password")

    if st.button("Create Account"):
        if role == "Admin" and super_code != SUPER_ADMIN_PASSWORD:
            st.error("Wrong admin key")
            return

        if add_user(email, password, role.lower()):
            st.success("Account created successfully")
        else:
            st.error("User already exists")
