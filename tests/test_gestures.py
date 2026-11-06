import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from gesture_utils import get_gesture, get_finger_state
from config import GESTURE_ACTIONS
import actions

def test_gesture_mapping_fist():
    assert get_gesture([0, 0, 0, 0, 0]) == "FIST"

def test_gesture_mapping_v_sign():
    assert get_gesture([0, 1, 1, 0, 0]) == "V_SIGN"

def test_gesture_mapping_open_palm():
    assert get_gesture([1, 1, 1, 1, 1]) == "OPEN_PALM"

def test_gesture_mapping_thumbs_up():
    assert get_gesture([1, 0, 0, 0, 0]) == "THUMBS_UP"

def test_gesture_mapping_one():
    assert get_gesture([0, 1, 0, 0, 0]) == "ONE"

def test_gesture_mapping_three():
    assert get_gesture([0, 1, 1, 1, 0]) == "THREE"

def test_gesture_mapping_four():
    assert get_gesture([0, 1, 1, 1, 1]) == "FOUR"

def test_gesture_mapping_gun_sign():
    assert get_gesture([1, 1, 0, 0, 0]) == "GUN_SIGN"

def test_gesture_mapping_rock_sign():
    assert get_gesture([1, 0, 0, 0, 1]) == "ROCK_SIGN"

def test_gesture_mapping_middle_only():
    assert get_gesture([0, 0, 1, 0, 0]) == "MIDDLE_ONLY"

def test_gesture_mapping_unknown():
    assert get_gesture([0, 0, 0, 1, 1]) == "UNKNOWN"

def test_finger_state_calculation():
    # Synthetic landmarks for open hand where fingertips are higher (lower y) than PIP joints
    landmarks = [(100, 100)] * 21
    # thumb tip (4) x > ip (3) x
    landmarks[4] = (150, 100)
    landmarks[3] = (120, 100)

    # other tips (8, 12, 16, 20) y < PIP (6, 10, 14, 18) y
    for tip, pip in [(8, 6), (12, 10), (16, 14), (20, 18)]:
        landmarks[tip] = (100, 50)
        landmarks[pip] = (100, 120)

    state = get_finger_state(landmarks)
    assert state == [1, 1, 1, 1, 1]
    assert get_gesture(state) == "OPEN_PALM"

def test_gesture_actions_configuration():
    assert len(GESTURE_ACTIONS) >= 10
    for gesture, action in GESTURE_ACTIONS.items():
        assert callable(action)

def test_action_execution_safe():
    # Verify that invoking action functions completes without throwing errors
    actions.open_calculator()
    actions.open_notepad()
    actions.open_browser()
