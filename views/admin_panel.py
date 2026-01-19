import streamlit as st
import pandas as pd
from db import (
    get_conn,
    add_user,
    delete_user,
    get_detections,
    get_logs
)

def admin_panel():
    st.title("Admin Panel")

    # ================= USERS =================
    st.subheader("User Management")

    conn = get_conn()
    users = conn.execute(
        "SELECT id,email,role FROM users ORDER BY id DESC"
    ).fetchall()
    conn.close()

    df_users = pd.DataFrame(
        users, columns=["ID", "Email", "Role"]
    ) if users else pd.DataFrame()

    st.dataframe(df_users, use_container_width=True)

    # ---- ADD USER ----
    st.markdown("Add New User")
    email = st.text_input("Email", key="add_email")
    password = st.text_input("Password", type="password", key="add_pass")
    role = st.selectbox("Role", ["user", "admin"])

    if st.button("Add User"):
        if add_user(email, password, role):
            st.success("User added successfully")
            st.experimental_rerun()
        else:
            st.error("User already exists")

    # ---- DELETE USER ----
    
    st.markdown("Delete User")

    if not df_users.empty:
        user_id = st.selectbox(
            "Select User ID to Delete",
            df_users["ID"].tolist()
        )

        if st.button("Delete User"):
            if st.session_state.email == "admin@admin.com" or st.session_state.role == "admin":
                delete_user(user_id)
                st.success("User deleted")
                st.experimental_rerun()
            else:
                st.error("Not authorized")

    st.markdown("---")

    # ================= LOGS =================
    st.subheader("System Logs")

    logs = get_logs(200)

    if logs.empty:
        st.info("No logs available")
    else:
        st.dataframe(logs, use_container_width=True)

    st.markdown("---")

    # ================= EXPORT =================
    st.subheader("Export Detection Data")

    df = get_detections()
    st.download_button(
        "Download Detections CSV",
        df.to_csv(index=False),
        "detections.csv",
        mime="text/csv"
    )
