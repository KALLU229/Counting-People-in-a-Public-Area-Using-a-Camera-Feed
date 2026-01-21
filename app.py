import streamlit as st
from db import init_db, create_default_admin
from views.login import login_page
from views.register import register_page
from views.dashboard import dashboard
from views.detection import detection_page
from views.live_camera import live_camera_page
from views.admin_panel import admin_panel
from config import ALERT_LIMIT




# ================== APP INIT ==================
st.set_page_config(
    page_title="Crowd Counting System",
    layout="wide"
)

init_db()
create_default_admin()


# ================== SESSION ==================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = None

if "email" not in st.session_state:
    st.session_state.email = None


# ================== AUTH FLOW ==================
if not st.session_state.logged_in:
    auth_page = st.sidebar.radio("Authentication", ["Login", "Register"])

    if auth_page == "Login":
        login_page()
    else:
        register_page()

else:
    # -------- SIDEBAR --------
    st.sidebar.success(f"Logged in as {st.session_state.email}")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.role = None
        st.session_state.email = None
        st.experimental_rerun()

    # -------- MENU --------
    menu = ["Dashboard", "Detection", "Live Camera"]
    if st.session_state.role == "admin":
        menu.append("Admin Panel")

    selected = st.sidebar.radio("Menu", menu)

    # -------- ROUTING --------
    if selected == "Dashboard":
        dashboard()

    elif selected == "Detection":
        detection_page()

    elif selected == "Live Camera":
        live_camera_page()

    elif selected == "Admin Panel":
        admin_panel()
