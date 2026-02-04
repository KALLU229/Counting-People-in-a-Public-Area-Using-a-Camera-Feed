import streamlit as st
import pandas as pd
from db import (
    get_conn,
    add_user,
    delete_user,
    get_detections,
    get_logs,
    get_alert_limit,
    set_alert_limit
)

def admin_panel():
    # ================= DARK ADMIN THEME STYLING =================
    st.markdown("""
        <style>
        /* Hide default elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Dark admin background - solid color, no image */
        .stApp {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%) !important;
        }
        
        /* Admin panel title */
        .admin-title {
            text-align: center;
            font-weight: 800;
            font-size: 42px;
            color: #00bcd4;
            text-shadow: 0 0 25px rgba(0, 188, 212, 0.5);
            margin-bottom: 2rem;
            letter-spacing: 1px;
            padding: 1rem;
            border-bottom: 2px solid rgba(0, 188, 212, 0.3);
        }
        
        /* Section headers */
        h3 {
            color: #80deea !important;
            font-weight: 600 !important;
            font-size: 24px !important;
            margin-top: 2rem !important;
            margin-bottom: 1rem !important;
            padding-bottom: 0.5rem !important;
            border-bottom: 1px solid rgba(0, 188, 212, 0.2) !important;
        }
        
        /* Subheaders/markdown headers */
        .stMarkdown h4, .stMarkdown p strong {
            color: #b2ebf2 !important;
            font-weight: 500 !important;
            font-size: 16px !important;
        }
        
        /* Input fields */
        .stTextInput > div > div > input,
        .stSelectbox > div > div > select {
            background-color: rgba(30, 41, 59, 0.8) !important;
            border: 1.5px solid rgba(0, 188, 212, 0.3) !important;
            border-radius: 8px !important;
            padding: 12px 16px !important;
            font-size: 15px !important;
            color: #e0f7fa !important;
            transition: all 0.2s ease !important;
        }
        
        .stTextInput > div > div > input:focus,
        .stSelectbox > div > div > select:focus {
            border-color: #00bcd4 !important;
            box-shadow: 0 0 0 3px rgba(0, 188, 212, 0.15) !important;
        }
        
        /* Labels */
        .stTextInput > label,
        .stSelectbox > label {
            color: #80deea !important;
            font-weight: 500 !important;
            font-size: 14px !important;
        }
        
        /* Buttons */
        .stButton > button {
            background: linear-gradient(135deg, #00bcd4 0%, #0097a7 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 12px 24px !important;
            font-size: 15px !important;
            font-weight: 600 !important;
            cursor: pointer !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 3px 12px rgba(0, 188, 212, 0.3) !important;
            text-transform: uppercase !important;
            letter-spacing: 0.5px !important;
        }
        
        .stButton > button:hover {
            background: linear-gradient(135deg, #00acc1 0%, #00838f 100%) !important;
            box-shadow: 0 5px 16px rgba(0, 188, 212, 0.4) !important;
            transform: translateY(-2px) !important;
        }
        
        /* Download button */
        .stDownloadButton > button {
            background: linear-gradient(135deg, #7c4dff 0%, #651fff 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 12px 24px !important;
            font-size: 15px !important;
            font-weight: 600 !important;
            cursor: pointer !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 3px 12px rgba(124, 77, 255, 0.3) !important;
        }
        
        .stDownloadButton > button:hover {
            background: linear-gradient(135deg, #651fff 0%, #6200ea 100%) !important;
            box-shadow: 0 5px 16px rgba(124, 77, 255, 0.4) !important;
            transform: translateY(-2px) !important;
        }
        
        /* Dataframe styling */
        .stDataFrame {
            background-color: rgba(30, 41, 59, 0.6) !important;
            border-radius: 10px !important;
            overflow: hidden !important;
            border: 1px solid rgba(0, 188, 212, 0.2) !important;
        }
        
        /* Dataframe headers */
        .stDataFrame thead tr th {
            background-color: rgba(0, 188, 212, 0.2) !important;
            color: #00bcd4 !important;
            font-weight: 600 !important;
            border-bottom: 2px solid rgba(0, 188, 212, 0.4) !important;
        }
        
        /* Dataframe cells */
        .stDataFrame tbody tr td {
            color: #e0f7fa !important;
            border-bottom: 1px solid rgba(0, 188, 212, 0.1) !important;
        }
        
        /* Dataframe rows hover */
        .stDataFrame tbody tr:hover {
            background-color: rgba(0, 188, 212, 0.05) !important;
        }
        
        /* Alert boxes */
        .stAlert {
            background: rgba(30, 41, 59, 0.9) !important;
            backdrop-filter: blur(10px) !important;
            border-radius: 8px !important;
            border-left: 4px solid #00bcd4 !important;
            color: #b2ebf2 !important;
        }
        
        /* Success message */
        .stSuccess {
            background-color: rgba(0, 200, 83, 0.15) !important;
            color: #4ade80 !important;
            border-left: 4px solid #22c55e !important;
        }
        
        /* Error message */
        .stError {
            background-color: rgba(239, 68, 68, 0.15) !important;
            color: #fca5a5 !important;
            border-left: 4px solid #ef4444 !important;
        }
        
        /* Info message */
        .stInfo {
            background-color: rgba(0, 188, 212, 0.15) !important;
            color: #80deea !important;
            border-left: 4px solid #00bcd4 !important;
        }
        
        /* Divider */
        hr {
            border: none !important;
            border-top: 2px solid rgba(0, 188, 212, 0.3) !important;
            margin: 2.5rem 0 !important;
            box-shadow: 0 0 10px rgba(0, 188, 212, 0.2) !important;
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background-color: rgba(15, 23, 42, 0.95) !important;
            backdrop-filter: blur(10px) !important;
            border-right: 1px solid rgba(0, 188, 212, 0.2) !important;
        }
        
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
            color: #e0f7fa !important;
        }
        
        /* Card-like sections */
        .section-card {
            background: rgba(30, 41, 59, 0.5);
            padding: 1.5rem;
            border-radius: 12px;
            border: 1px solid rgba(0, 188, 212, 0.2);
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        }
        </style>
    """, unsafe_allow_html=True)

    # ================= TITLE =================
    st.markdown(
        """
        <h1 class="admin-title">
             Admin Control Panel
        </h1>
        """,
        unsafe_allow_html=True
    )

    # ================= USERS =================
    st.subheader(" User Management")

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
    st.markdown("#### Add New User")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        email = st.text_input("Email", key="add_email", placeholder="user@example.com")
    with col2:
        password = st.text_input("Password", type="password", key="add_pass", placeholder="••••••••")
    with col3:
        role = st.selectbox("Role", ["user", "admin"])

    if st.button(" Add User", use_container_width=True):
        if not email or not password:
            st.error(" Please enter both email and password")
        elif add_user(email, password, role):
            st.success(" User added successfully")
            st.rerun()
        else:
            st.error(" User already exists")

    # ---- DELETE USER ----
    st.markdown("####  Delete User")

    if not df_users.empty:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            user_id = st.selectbox(
                "Select User ID to Delete",
                df_users["ID"].tolist()
            )
        
        with col2:
            st.write("")  # Spacing
            st.write("")  # Spacing
            if st.button(" Delete User", use_container_width=True):
                if st.session_state.email == "admin@admin.com" or st.session_state.role == "admin":
                    delete_user(user_id)
                    st.success(" User deleted successfully")
                    st.rerun()
                else:
                    st.error("Not authorized to delete users")
    else:
        st.info(" No users available to delete")

    # ================= SYSTEM SETTINGS =================
    st.markdown("---")
    st.subheader(" System Settings")

    # current value from DB
    current_limit = get_alert_limit()
    new_limit = st.number_input("Crowd Alert Threshold", min_value=1, max_value=10000, value=current_limit, step=1)

    if st.button(" Save Threshold", use_container_width=True):
        set_alert_limit(int(new_limit))
        st.success(f" Alert threshold updated to {new_limit}")
        st.rerun()

    st.markdown("---")

    # ================= LOGS =================
    st.subheader(" System Logs")

    logs = get_logs(200)

    if logs.empty:
        st.info(" No logs available")
    else:
        st.dataframe(logs, use_container_width=True, height=400)

    st.markdown("---")

    # ================= EXPORT =================
    st.subheader(" Export Detection Data")

    df = get_detections()
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown(f"**Total detections available:** {len(df)}")
    
    with col2:
        st.download_button(
            " Download CSV",
            df.to_csv(index=False),
            "detections.csv",
            mime="text/csv",
            use_container_width=True
        )