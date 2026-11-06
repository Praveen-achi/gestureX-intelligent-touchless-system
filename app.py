import streamlit as st
import cv2
import mediapipe as mp
import time
import os
import sys

from gesture_utils import get_finger_state, get_gesture
from config import GESTURE_ACTIONS

st.set_page_config(page_title="GestureX - Intelligent Touchless System", layout="wide", page_icon="🖐")

st.title("🖐 GestureX - Intelligent Touchless HCI System")
st.markdown("Control your desktop applications seamlessly using real-time computer vision and hand gesture recognition.")

# Sidebar diagnostics & mode selection
st.sidebar.header("⚙️ Configuration & Diagnostics")
app_mode = st.sidebar.radio(
    "Choose Mode:",
    ["Live Camera Mode", "Gesture Action Simulator (Docker / Cloud CI)"]
)

is_container = os.path.exists("/.dockerenv") or os.environ.get("STREAMLIT_SERVER_HEADLESS") == "true"
if is_container:
    st.sidebar.success("🐳 Running inside Docker Container")
else:
    st.sidebar.info(f"💻 Running on Host ({sys.platform})")

st.sidebar.markdown("### 📋 Supported Gestures")
for g, act in GESTURE_ACTIONS.items():
    st.sidebar.markdown(f"- **{g}** ➔ `{act.__name__}`")

GESTURE_HOLD_TIME = 2

if app_mode == "Live Camera Mode":
    st.subheader("📹 Real-Time Webcam Gesture Detection")
    run = st.checkbox("Start Camera")
    FRAME_WINDOW = st.image([])

    mp_hands = mp.solutions.hands

    gesture_start_time = None
    current_gesture = None
    action_triggered = False

    status_placeholder = st.empty()

    if run:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            st.error("⚠️ No camera device detected or camera access is restricted. If running in Docker, pass `--device=/dev/video0` or switch to the Simulator mode.")
        else:
            with mp_hands.Hands(
                max_num_hands=1,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5
            ) as hands:
                while run:
                    ret, frame = cap.read()
                    if not ret:
                        st.error("Camera feed stopped.")
                        break

                    frame = cv2.flip(frame, 1)
                    frame = cv2.convertScaleAbs(frame, alpha=1.2, beta=20)
                    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                    result = hands.process(rgb)

                    gesture_text = "None"
                    finger_state = []
                    status = "Waiting for gesture..."

                    if result.multi_hand_landmarks:
                        for handLms in result.multi_hand_landmarks:
                            h, w, _ = frame.shape
                            landmarks = []

                            for lm in handLms.landmark:
                                landmarks.append((int(lm.x * w), int(lm.y * h)))

                            finger_state = get_finger_state(landmarks)
                            gesture_text = get_gesture(finger_state)

                            # Stability Logic
                            if gesture_text == current_gesture and gesture_text != "UNKNOWN":
                                if gesture_start_time is None:
                                    gesture_start_time = time.time()

                                elapsed = time.time() - gesture_start_time

                                if elapsed > GESTURE_HOLD_TIME and not action_triggered:
                                    status = f"✅ Action Triggered: {gesture_text} ➔ {GESTURE_ACTIONS.get(gesture_text, lambda: None).__name__}"
                                    action = GESTURE_ACTIONS.get(gesture_text)
                                    if action:
                                        action()
                                    action_triggered = True
                                else:
                                    status = f"Holding '{gesture_text}' ({elapsed:.1f}s / {GESTURE_HOLD_TIME}s)..."
                            else:
                                current_gesture = gesture_text
                                gesture_start_time = None
                                action_triggered = False

                    status_placeholder.markdown(f"**Gesture:** `{gesture_text}` | **Finger Pattern:** `{finger_state}` | **Status:** {status}")
                    FRAME_WINDOW.image(rgb)

            cap.release()

elif app_mode == "Gesture Action Simulator (Docker / Cloud CI)":
    st.subheader("🧪 Gesture Action Simulator")
    st.info("This mode allows testing touchless actions without needing a physical webcam, ideal for Docker environments, CI/CD pipelines, and cloud instances.")

    col1, col2 = st.columns([1, 1])

    with col1:
        selected_gesture = st.selectbox("Select Gesture to Simulate:", list(GESTURE_ACTIONS.keys()))
        trigger_btn = st.button("🚀 Trigger Action", type="primary")

    with col2:
        st.markdown(f"**Mapped Action:** `{GESTURE_ACTIONS[selected_gesture].__name__}`")
        if trigger_btn:
            action_func = GESTURE_ACTIONS[selected_gesture]
            action_func()
            st.success(f"Successfully executed action `{action_func.__name__}` for gesture `{selected_gesture}`!")
