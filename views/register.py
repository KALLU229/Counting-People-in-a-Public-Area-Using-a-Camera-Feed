import streamlit as st
from db import add_user

SUPER_ADMIN_PASSWORD = "kalludon"

def register_page():
    # ───────────────────────────────────────────────
    # Page config - centered layout
    # ───────────────────────────────────────────────
    st.set_page_config(
        page_title="Register | Your App",
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

/* Cinematic dark overlay */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(circle at 25% 20%, rgba(0,188,212,0.08), transparent 40%),
        radial-gradient(circle at 75% 80%, rgba(0,188,212,0.06), transparent 45%),
        rgba(8, 14, 22, 0.85);
    z-index: 0;
    pointer-events: none;
}

/* Ensure content is above overlay */
.main .block-container {
    position: relative;
    z-index: 1;
}

/* ================= REGISTER CARD ================= */
.register-card {
    background: linear-gradient(
        180deg,
        rgba(22, 38, 56, 0.94),
        rgba(14, 28, 42, 0.94)
    );
    backdrop-filter: blur(22px);
    -webkit-backdrop-filter: blur(22px);
    padding: 3.2rem 2.8rem;
    border-radius: 22px;
    max-width: 480px;
    margin: 4rem auto 2rem;
    border: 1px solid rgba(0, 188, 212, 0.28);
    box-shadow:
        0 28px 65px rgba(0, 0, 0, 0.7),
        inset 0 0 0 1px rgba(255,255,255,0.03),
        inset 0 0 45px rgba(0,188,212,0.07);
}

/* ================= TITLE ================= */
.register-title {
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
    background-color: rgba(24, 42, 60, 0.78);
    border: 1.6px solid rgba(0, 188, 212, 0.38);
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
        0 0 30px rgba(0, 229, 255, 0.45);
}

/* Labels */
.stTextInput > label,
.stRadio > label {
    color: #9be9f2;
    font-weight: 600;
    font-size: 14px;
    margin-bottom: 8px;
}

/* ================= RADIO GROUP ================= */
.stRadio > div {
    background: rgba(20, 36, 52, 0.65);
    padding: 14px;
    border-radius: 12px;
    border: 1px solid rgba(0, 188, 212, 0.25);
}

.stRadio label {
    color: #c7f4fb;
    padding: 10px 16px;
    border-radius: 10px;
    transition: all 0.25s ease;
}

.stRadio label:hover {
    background: rgba(0, 188, 212, 0.12);
}

/* ================= INFO BOX ================= */
.info-box {
    background: rgba(0, 229, 255, 0.12);
    border-left: 4px solid #00e5ff;
    padding: 14px 18px;
    border-radius: 10px;
    color: #bff6ff;
    margin-top: 1.2rem;
    font-size: 13.5px;
    box-shadow: inset 0 0 12px rgba(0,188,212,0.15);
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
        0 12px 36px rgba(0, 229, 255, 0.65),
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
    background-color: rgba(8, 14, 22, 0.97);
    backdrop-filter: blur(14px);
    border-right: 1px solid rgba(0, 188, 212, 0.28);
}

[data-testid="stSidebar"] * {
    color: #e6faff;
}

</style>
""", unsafe_allow_html=True)


    # ───────────────────────────────────────────────
    # Register UI – centered card
    # ───────────────────────────────────────────────
    with st.container():
        st.markdown('<div class="register-card">', unsafe_allow_html=True)
        
        st.markdown('<div class="register-title">Create Account</div>', unsafe_allow_html=True)
        
        email = st.text_input("Email", placeholder="name@example.com")
        password = st.text_input("Password", type="password", placeholder="••••••••")
        role = st.radio("Register as", ["User", "Admin"])

        super_code = None
        if role == "Admin":
            st.markdown(
                '<div class="info-box">Admin registration requires a super password</div>',
                unsafe_allow_html=True
            )
            super_code = st.text_input("Super Password", type="password", placeholder="Enter admin key")

        if st.button("Create Account", use_container_width=True):
            if not email or not password:
                st.error("Please enter both email and password")
            elif role == "Admin" and super_code != SUPER_ADMIN_PASSWORD:
                st.error("Wrong admin key")
            else:
                if add_user(email, password, role.lower()):
                    st.success("Account created successfully!")
                else:
                    st.error("User already exists")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Optional footer
    st.markdown(
        '<div class="custom-footer">'
        '© 2026 • All rights reserved By KALLUDON'
        '</div>',
        unsafe_allow_html=True
    )