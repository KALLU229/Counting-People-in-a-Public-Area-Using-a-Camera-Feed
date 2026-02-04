import streamlit as st
import cv2
import tempfile
from vision.process_frame import process_frame, reset_tracker
from db import get_alert_limit

reset_tracker()

def detection_page():
    # ================= DARK DETECTION THEME STYLING =================
    st.markdown("""
        <style>
        /* Hide default elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Dark solid background */
        .stApp {
            background: linear-gradient(135deg, #0a0e1a 0%, #1a1f35 100%) !important;
        }
        
        /* Detection page title */
        .detection-title {
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
        
        /* File uploader */
        [data-testid="stFileUploader"] {
            background: rgba(30, 41, 59, 0.6) !important;
            border: 2px dashed rgba(0, 188, 212, 0.4) !important;
            border-radius: 12px !important;
            padding: 2rem !important;
        }
        
        [data-testid="stFileUploader"] label {
            color: #80deea !important;
            font-weight: 600 !important;
            font-size: 16px !important;
        }
        
        [data-testid="stFileUploader"] section {
            border: none !important;
        }
        
        /* Upload button */
        [data-testid="stFileUploader"] button {
            background: linear-gradient(135deg, #00bcd4 0%, #0097a7 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 10px 20px !important;
            font-weight: 600 !important;
        }
        
        /* Metric cards */
        [data-testid="stMetricValue"] {
            font-size: 36px !important;
            color: #00bcd4 !important;
            font-weight: 700 !important;
            text-shadow: 0 0 15px rgba(0, 188, 212, 0.5);
        }
        
        [data-testid="stMetricLabel"] {
            color: #80deea !important;
            font-size: 16px !important;
            font-weight: 600 !important;
            letter-spacing: 2px;
        }
        
        /* Metric containers */
        [data-testid="metric-container"] {
            background: rgba(20, 35, 50, 0.8) !important;
            backdrop-filter: blur(15px);
            padding: 1.5rem !important;
            border-radius: 15px !important;
            border: 1px solid rgba(0, 188, 212, 0.3) !important;
            box-shadow: 
                0 4px 20px rgba(0, 0, 0, 0.3),
                0 0 40px rgba(0, 188, 212, 0.1) !important;
        }
        
        /* Video frame container */
        .stImage {
            border-radius: 12px !important;
            overflow: hidden !important;
            border: 2px solid rgba(0, 188, 212, 0.3) !important;
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.5) !important;
        }
        
        /* Alert boxes */
        .stAlert {
            background: rgba(30, 41, 59, 0.9) !important;
            backdrop-filter: blur(10px) !important;
            border-radius: 10px !important;
            border-left: 4px solid #00bcd4 !important;
            color: #b2ebf2 !important;
            font-weight: 500 !important;
        }
        
        /* Success message */
        .stSuccess {
            background-color: rgba(0, 200, 83, 0.2) !important;
            color: #4ade80 !important;
            border-left: 4px solid #22c55e !important;
            font-weight: 600 !important;
        }
        
        /* Error/Alert message */
        .stError {
            background-color: rgba(239, 68, 68, 0.2) !important;
            color: #ff5252 !important;
            border-left: 4px solid #ef4444 !important;
            font-weight: 700 !important;
            animation: pulse 1.5s ease-in-out infinite;
        }
        
        /* Info message */
        .stInfo {
            background-color: rgba(0, 188, 212, 0.15) !important;
            color: #80deea !important;
            border-left: 4px solid #00bcd4 !important;
        }
        
        /* Pulse animation for alerts */
        @keyframes pulse {
            0%, 100% {
                box-shadow: 0 0 10px rgba(239, 68, 68, 0.3);
            }
            50% {
                box-shadow: 0 0 25px rgba(239, 68, 68, 0.6);
            }
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
        
        /* Status indicator */
        .status-box {
            background: rgba(30, 41, 59, 0.8);
            padding: 1rem;
            border-radius: 10px;
            border-left: 4px solid #00bcd4;
            margin: 1rem 0;
            color: #b2ebf2;
        }
        
        /* Processing status */
        .processing-status {
            text-align: center;
            color: #00bcd4;
            font-size: 18px;
            font-weight: 600;
            padding: 1rem;
            background: rgba(0, 188, 212, 0.1);
            border-radius: 8px;
            margin: 1rem 0;
        }
        </style>
    """, unsafe_allow_html=True)

    # ================= TITLE =================
    st.markdown(
        """
        <h1 class="detection-title">
            Video Upload Detection
        </h1>
        """,
        unsafe_allow_html=True
    )

    # ================= FILE UPLOADER =================
    uploaded = st.file_uploader(
        " Upload Video File",
        type=["mp4", "avi", "mov", "mkv"],
        help="Supported formats: MP4, AVI, MOV, MKV"
    )

    if not uploaded:
        st.info("Please upload a video file to begin detection")
        st.markdown(
            """
            <div class="status-box">
                <strong> Instructions:</strong>
                <ul>
                    <li>Upload a video file using the uploader above</li>
                    <li>Supported formats: MP4, AVI, MOV, MKV</li>
                    <li>The system will automatically detect and count people</li>
                    <li>Alert will trigger if crowd exceeds the limit</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )
        return

    # ================= PROCESSING SECTION =================
    st.markdown('<div class="processing-status"> Processing video...</div>', unsafe_allow_html=True)
    
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded.read())

    cap = cv2.VideoCapture(tfile.name)
    frame_window = st.empty()
    status_container = st.empty()

    # Reset tracker and alert state so each uploaded video starts fresh
    reset_tracker()
    st.session_state.alert_triggered = False
    status_container.empty()

    total_in = total_out = 0

    ok, frame = cap.read()
    if not ok:
        st.error(" Cannot read video file. Please try a different video.")
        return

    h, w = frame.shape[:2]
    line_y = h // 2

    # ================= METRICS PLACEHOLDER =================
    metrics_cols = st.columns(3)

    while ok:
        ok, frame = cap.read()
        if not ok:
            break

        frame, total_in, total_out, inside = process_frame(
            frame, h, w, line_y, total_in, total_out
        )

        # ================= ALERT SYSTEM =================
        if "alert_triggered" not in st.session_state:
            st.session_state.alert_triggered = False

        # Fetch live alert threshold (allows admin to change it at runtime)
        current_limit = get_alert_limit()

        if inside >= current_limit and not st.session_state.alert_triggered:
            status_container.error(f" ALERT: Crowd limit exceeded! ({inside}/{current_limit})")
            st.session_state.alert_triggered = True
        elif inside < current_limit:
            st.session_state.alert_triggered = False
            status_container.empty()

        # ================= LIVE METRICS UPDATE =================
        with metrics_cols[0]:
            st.metric(" Entered", total_in)
        with metrics_cols[1]:
            st.metric(" Exited", total_out)
        with metrics_cols[2]:
            st.metric(" Inside", inside)

        # ================= DISPLAY FRAME =================
        frame_window.image(
            cv2.cvtColor(frame, cv2.COLOR_BGR2RGB),
            width=min(w, 800)
        )

    cap.release()
    # Reset alert state after processing to ensure next upload works
    st.session_state.alert_triggered = False

    # ================= COMPLETION STATUS =================
    st.success("Video processing completed successfully!")
    
    st.markdown("---")
    
    # ================= FINAL SUMMARY =================
    st.markdown(
        """
        <div class="status-box">
            <strong>Final Statistics</strong>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    summary_cols = st.columns(3)
    with summary_cols[0]:
        st.metric("Total Entered", total_in)
    with summary_cols[1]:
        st.metric("Total Exited", total_out)
    with summary_cols[2]:
        st.metric("Final Inside Count", inside)