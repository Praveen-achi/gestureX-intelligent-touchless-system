TIP_IDS = [4, 8, 12, 16, 20]

def get_finger_state(landmarks):
    fingers = []

    # Thumb
    fingers.append(1 if landmarks[4][0] > landmarks[3][0] else 0)

    # Other fingers
    for i in range(1, 5):
        fingers.append(1 if landmarks[TIP_IDS[i]][1] < landmarks[TIP_IDS[i]-2][1] else 0)

    return fingers


def get_gesture(fingers):
    gesture_map = {
        (0,0,0,0,0): "FIST",
        (0,1,1,0,0): "V_SIGN",
        (1,0,0,0,0): "THUMBS_UP",
        (1,1,1,1,1): "OPEN_PALM",
        (0,1,0,0,0): "ONE",
        (0,1,1,1,0): "THREE",
        (0,1,1,1,1): "FOUR",
        (1,1,0,0,0): "GUN_SIGN",
        (1,0,0,0,1): "ROCK_SIGN",
        (0,0,1,0,0): "MIDDLE_ONLY"
    }

    return gesture_map.get(tuple(fingers), "UNKNOWN")

