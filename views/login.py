import streamlit as st
from db import validate_user

def login_page():
    # ───────────────────────────────────────────────
    # Page config - centered layout, no forced sidebar collapse
    # ───────────────────────────────────────────────
    st.set_page_config(
        page_title="Login | Your App",
        layout="centered"
    )

    # ───────────────────────────────────────────────
    # Dark theme CSS with network background image
    # ───────────────────────────────────────────────
    st.markdown("""
<style>

/* Hide Streamlit menu & footer */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* ================= BACKGROUND ================= */
.stApp {
    background-image: url('https://i.ibb.co/8DQ3y517/image.png');
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}

/* Dark cinematic overlay */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(circle at 20% 20%, rgba(0,188,212,0.08), transparent 40%),
        radial-gradient(circle at 80% 80%, rgba(0,188,212,0.05), transparent 45%),
        rgba(10, 18, 28, 0.82);
    z-index: 0;
    pointer-events: none;
}

/* Keep content above overlay */
.main .block-container {
    position: relative;
    z-index: 1;
}

/* ================= LOGIN CARD ================= */
.login-card {
    background: linear-gradient(
        180deg,
        rgba(22, 38, 56, 0.92),
        rgba(16, 30, 44, 0.92)
    );
    backdrop-filter: blur(22px);
    -webkit-backdrop-filter: blur(22px);
    padding: 3.2rem 2.8rem;
    border-radius: 22px;
    max-width: 430px;
    margin: 4.5rem auto 2rem;
    border: 1px solid rgba(0, 188, 212, 0.25);
    box-shadow:
        0 25px 60px rgba(0, 0, 0, 0.65),
        inset 0 0 0 1px rgba(255,255,255,0.03),
        inset 0 0 40px rgba(0,188,212,0.06);
}

/* ================= TITLE ================= */
.login-title {
    color: #00e5ff;
    font-size: 34px;
    font-weight: 800;
    text-align: center;
    margin-bottom: 2.4rem;
    letter-spacing: 0.6px;
    text-shadow:
        0 0 25px rgba(0, 229, 255, 0.55),
        0 0 60px rgba(0, 188, 212, 0.35);
}

/* ================= INPUTS ================= */
.stTextInput > div > div > input {
    background-color: rgba(24, 42, 60, 0.75);
    border: 1.6px solid rgba(0, 188, 212, 0.35);
    border-radius: 12px;
    padding: 15px 18px;
    font-size: 15px;
    color: #e6faff;
    transition: all 0.3s ease;
}

.stTextInput > div > div > input::placeholder {
    color: rgba(230, 250, 255, 0.35);
}

.stTextInput > div > div > input:focus {
    border-color: #00e5ff;
    background-color: rgba(24, 42, 60, 0.95);
    box-shadow:
        0 0 0 3px rgba(0, 229, 255, 0.18),
        0 0 28px rgba(0, 229, 255, 0.45);
}

/* Labels */
.stTextInput > label {
    color: #9be9f2;
    font-weight: 600;
    font-size: 14px;
    margin-bottom: 8px;
}

/* ================= BUTTON ================= */
.stButton > button {
    background: linear-gradient(135deg, #00e5ff, #00acc1);
    color: #02131a;
    border-radius: 12px;
    padding: 16px 24px;
    font-size: 16px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    border: none;
    margin-top: 1.8rem;
    transition: all 0.3s ease;
    box-shadow:
        0 8px 24px rgba(0, 229, 255, 0.45),
        0 0 40px rgba(0, 188, 212, 0.35);
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow:
        0 12px 35px rgba(0, 229, 255, 0.65),
        0 0 55px rgba(0, 188, 212, 0.45);
}

.stButton > button:active {
    transform: translateY(0);
}

/* ================= ALERTS ================= */
.stAlert {
    border-radius: 12px;
    border: none;
    margin-top: 1.2rem;
    backdrop-filter: blur(12px);
}

.stSuccess {
    background: rgba(34, 197, 94, 0.18);
    color: #86efac;
    border-left: 4px solid #22c55e;
}

.stError {
    background: rgba(239, 68, 68, 0.18);
    color: #fca5a5;
    border-left: 4px solid #ef4444;
}

/* ================= FOOTER ================= */
.custom-footer {
    text-align: center;
    color: #7dd3fc;
    font-size: 13px;
    margin-top: 3.5rem;
    padding-bottom: 2rem;
    letter-spacing: 0.4px;
    text-shadow: 0 2px 12px rgba(0,0,0,0.9);
}

/* ================= SIDEBAR ================= */
[data-testid="stSidebar"] {
    background-color: rgba(10, 18, 28, 0.96);
    backdrop-filter: blur(14px);
    border-right: 1px solid rgba(0, 188, 212, 0.25);
}

[data-testid="stSidebar"] * {
    color: #e6faff;
}

</style>
""", unsafe_allow_html=True)


    # ───────────────────────────────────────────────
    # Login UI – centered card
    # ───────────────────────────────────────────────
    with st.container():
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        
        st.markdown('<div class="login-title">Sign In</div>', unsafe_allow_html=True)
        
        email = st.text_input("Email", placeholder="name@example.com")
        password = st.text_input("Password", type="password", placeholder="••••••••")
        
        if st.button("Login", use_container_width=True):
            if not email or not password:
                st.error("Please enter both email and password")
            else:
                with st.spinner("Authenticating..."):
                    user = validate_user(email, password)
                    if user:
                        st.session_state.logged_in = True
                        st.session_state.role = user.get("role", "user")
                        st.session_state.email = user["email"]
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Invalid credentials")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Optional footer
    st.markdown(
        '<div class="custom-footer">'
        '© 2026 Your • All rights reserved By KALLUDON'
        '</div>',
        unsafe_allow_html=True
    )