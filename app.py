import streamlit as st
import cv2
import mediapipe as mp
import time

from gesture_utils import get_finger_state, get_gesture
from config import GESTURE_ACTIONS

st.set_page_config(page_title="Gesture Control", layout="wide")

st.title("🖐 Advanced Gesture-Based HCI System")

run = st.checkbox("Start Camera")

FRAME_WINDOW = st.image([])

mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)

gesture_start_time = None
current_gesture = None
action_triggered = False

GESTURE_HOLD_TIME = 2

with mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
) as hands:

    while run:
        ret, frame = cap.read()
        if not ret:
            st.error("Camera not working")
            break

        frame = cv2.flip(frame, 1)

        # Improve brightness/contrast
        frame = cv2.convertScaleAbs(frame, alpha=1.2, beta=20)

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        result = hands.process(rgb)

        gesture_text = "None"
        finger_state = []
        status = "Waiting..."

        if result.multi_hand_landmarks:
            for handLms in result.multi_hand_landmarks:
                h, w, _ = frame.shape
                landmarks = []

                for lm in handLms.landmark:
                    landmarks.append((int(lm.x * w), int(lm.y * h)))

                finger_state = get_finger_state(landmarks)
                gesture_text = get_gesture(finger_state)

                # Stability Logic
                if gesture_text == current_gesture:
                    if gesture_start_time is None:
                        gesture_start_time = time.time()

                    elapsed = time.time() - gesture_start_time

                    if elapsed > GESTURE_HOLD_TIME and not action_triggered:
                        status = "Action Triggered"

                        action = GESTURE_ACTIONS.get(gesture_text)

                        if action:
                            action()

                        action_triggered = True

                else:
                    current_gesture = gesture_text
                    gesture_start_time = None
                    action_triggered = False

        # UI
        st.write(f"Gesture: {gesture_text}")
        st.write(f"Finger Pattern: {finger_state}")
        st.write(f"Status: {status}")

        FRAME_WINDOW.image(rgb)

cap.release()

##cd C:\Users\navan\Documents\co2_streamlit_app\gesture_based_webos
# venv\Scripts\activate
# streamlit run app.py