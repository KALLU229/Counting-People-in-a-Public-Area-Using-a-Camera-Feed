import streamlit as st
import cv2
from vision.process_frame import process_frame, reset_tracker
from db import get_alert_limit

# ================= CONFIG =================
USE_CAMERA_INDEX = 0
reset_tracker()


def live_camera_page():

    # -------- CLEAR PREVIOUS PAGE CONTENT --------
    st.empty()

    # -------- PAGE STATE CONTROL --------
    if "run_camera" not in st.session_state:
        st.session_state.run_camera = True

    # Reset tracker when (re)starting the live camera so old IDs don't persist
    reset_tracker()

    # ================= DARK UI STYLING =================
    st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    .stApp {
        background: radial-gradient(circle at top, #111827 0%, #020617 60%);
    }

    .camera-title {
        text-align: center;
        font-weight: 800;
        font-size: 40px;
        color: #22d3ee;
        margin: 1.5rem 0 2rem;
        letter-spacing: 1px;
        text-shadow: 0 0 30px rgba(34, 211, 238, 0.45);
    }

    .live-indicator {
        display: inline-flex;
        align-items: center;
        gap: 10px;
        background: rgba(239, 68, 68, 0.18);
        padding: 0.55rem 1.6rem;
        border-radius: 999px;
        border: 1px solid rgba(239, 68, 68, 0.6);
        box-shadow: 0 0 25px rgba(239, 68, 68, 0.4);
    }

    .live-dot {
        width: 10px;
        height: 10px;
        background: #ef4444;
        border-radius: 50%;
    }

    .live-text {
        color: #fecaca;
        font-weight: 700;
        letter-spacing: 2px;
    }

    .stImage {
        border-radius: 16px !important;
        overflow: hidden !important;
        border: 2px solid rgba(34, 211, 238, 0.35) !important;
        box-shadow:
            0 18px 45px rgba(0, 0, 0, 0.7),
            0 0 55px rgba(34, 211, 238, 0.25) !important;
    }

    [data-testid="metric-container"] {
        background: linear-gradient(
            180deg,
            rgba(17, 24, 39, 0.9),
            rgba(2, 6, 23, 0.9)
        ) !important;
        border-radius: 16px !important;
        padding: 1.6rem !important;
        border: 1px solid rgba(34, 211, 238, 0.3) !important;
        box-shadow:
            0 10px 30px rgba(0, 0, 0, 0.6),
            inset 0 0 20px rgba(34, 211, 238, 0.08) !important;
    }

    [data-testid="stMetricValue"] {
        font-size: 34px !important;
        font-weight: 800 !important;
        color: #22d3ee !important;
    }

    [data-testid="stMetricLabel"] {
        color: #a5f3fc !important;
        font-size: 15px !important;
        font-weight: 600 !important;
        letter-spacing: 2px;
    }

    .stAlert {
        background: rgba(15, 23, 42, 0.92) !important;
        border-radius: 14px !important;
        border-left: 4px solid #22d3ee !important;
        color: #e0f7fa !important;
    }

    .stError {
        background: rgba(127, 29, 29, 0.35) !important;
        border-left: 4px solid #ef4444 !important;
        color: #fecaca !important;
        font-weight: 700 !important;
    }

    .stSuccess {
        background: rgba(20, 83, 45, 0.35) !important;
        border-left: 4px solid #22c55e !important;
        color: #86efac !important;
    }

    [data-testid="stSidebar"] {
        background: rgba(2, 6, 23, 0.98) !important;
        border-right: 1px solid rgba(34, 211, 238, 0.25) !important;
    }

    [data-testid="stSidebar"] * {
        color: #e0f7fa !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # ================= TITLE =================
    st.markdown('<h1 class="camera-title">Live Camera Tracking</h1>', unsafe_allow_html=True)

    # ================= LIVE BADGE =================
    st.markdown("""
        <div style="text-align:center; margin-bottom:1.5rem;">
            <div class="live-indicator">
                <div class="live-dot"></div>
                <span class="live-text">LIVE</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # ================= STOP BUTTON =================
    stop_col = st.columns([1, 2, 1])[1]
    with stop_col:
        if st.button("Stop Camera", use_container_width=True):
            st.session_state.run_camera = False

    # ================= CAMERA INIT =================
    cam = cv2.VideoCapture(USE_CAMERA_INDEX)
    if not cam.isOpened():
        st.error("Cannot access camera")
        return

    st.success("Camera connected successfully")

    # ================= FIXED LAYOUT =================
    video_container = st.container()
    status_container = st.empty()
    metrics_container = st.container()

    with video_container:
        frame_placeholder = st.empty()

    with metrics_container:
        col1, col2, col3 = st.columns(3)
        entered_metric = col1.empty()
        exited_metric = col2.empty()
        inside_metric = col3.empty()

    total_in = total_out = 0

    ok, frame = cam.read()
    if not ok:
        st.error("Cannot read from camera")
        cam.release()
        return

    h, w = frame.shape[:2]
    line_y = h // 2

    # ================= CAMERA LOOP =================
    try:
        while st.session_state.run_camera:
            ok, frame = cam.read()
            if not ok:
                break

            frame, total_in, total_out, inside = process_frame(
                frame, h, w, line_y, total_in, total_out
            )

            # -------- ALERT SYSTEM --------
            # fetch the current threshold so admins can change it live
            current_limit = get_alert_limit()
            if inside >= current_limit:
                status_container.error(
                    f"ALERT: Crowd limit exceeded! Current: {inside} | Limit: {current_limit}"
                )
            else:
                status_container.empty()

            # -------- UPDATE METRICS --------
            entered_metric.metric("Entered", total_in)
            exited_metric.metric("Exited", total_out)
            inside_metric.metric("Inside", inside)

            # -------- UPDATE VIDEO --------
            frame_placeholder.image(
                cv2.cvtColor(frame, cv2.COLOR_BGR2RGB),
                width=min(w, 800),
                caption="Live Camera Feed"
            )

    finally:
        cam.release()
        frame_placeholder.empty()
        metrics_container.empty()
        status_container.empty()
        st.info("Camera feed stopped")
