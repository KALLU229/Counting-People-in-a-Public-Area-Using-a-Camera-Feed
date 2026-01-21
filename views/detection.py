import streamlit as st
import cv2
import tempfile
from vision.process_frame import process_frame, reset_tracker
from config import ALERT_LIMIT

reset_tracker()

def detection_page():
    st.title("Video Upload Detection")

    uploaded = st.file_uploader(
        "Upload Video", type=["mp4", "avi", "mov", "mkv"]
    )

    if not uploaded:
        st.info("Upload a video to begin")
        return

    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded.read())

    cap = cv2.VideoCapture(tfile.name)
    frame_window = st.empty()

    total_in = total_out = 0

    ok, frame = cap.read()
    if not ok:
        st.error("Cannot read video")
        return

    h, w = frame.shape[:2]
    line_y = h // 2

    while ok:
        ok, frame = cap.read()
        if not ok:
            break

        frame, total_in, total_out, inside = process_frame(
            frame, h, w, line_y, total_in, total_out
        )
        # ================= SIMPLE ALERT SYSTEM =================

        if "alert_triggered" not in st.session_state:
            st.session_state.alert_triggered = False

        if inside >= ALERT_LIMIT and not st.session_state.alert_triggered:
            st.error("ALERT: Crowd limit exceeded!")
            st.session_state.alert_triggered = True

        elif inside < ALERT_LIMIT:
            st.session_state.alert_triggered = False

        frame_window.image(
            cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        )

    cap.release()

    st.success("Processing completed")
    st.metric("Entered", total_in)
    st.metric("Exited", total_out)
    st.metric("Inside", inside)
