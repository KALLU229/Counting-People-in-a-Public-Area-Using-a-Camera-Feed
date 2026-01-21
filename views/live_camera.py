import streamlit as st
import cv2
from vision.process_frame import process_frame, reset_tracker
from config import ALERT_LIMIT


USE_CAMERA_INDEX = 0
reset_tracker()

def live_camera_page():
    st.subheader("Live Camera Tracking")

    cam = cv2.VideoCapture(USE_CAMERA_INDEX)
    frame_window = st.empty()

    total_in = total_out = 0

    ok, frame = cam.read()
    h, w = frame.shape[:2]
    line_y = h // 2

    while ok:
        ok, frame = cam.read()
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

    cam.release()
