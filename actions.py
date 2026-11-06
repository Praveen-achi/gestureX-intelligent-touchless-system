import os
import sys
import webbrowser
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def _run_action(win_target, fallback_label="Action"):
    """
    Executes native Windows application command when running on Windows host.
    In container or non-Windows environments, safely logs and handles the action.
    """
    if sys.platform == "win32":
        try:
            os.system(f"start {win_target}")
        except Exception as e:
            logging.error(f"Error launching Windows target {win_target}: {e}")
    else:
        logging.info(f"[CONTAINER ACTION] Triggered '{fallback_label}' (target: '{win_target}')")

def open_camera():
    _run_action("microsoft.windows.camera:", fallback_label="Camera")

def open_notepad():
    _run_action("notepad", fallback_label="Notepad")

def open_calculator():
    _run_action("calc", fallback_label="Calculator")

def open_browser():
    try:
        webbrowser.open("https://www.google.com")
    except Exception:
        pass
    logging.info("[ACTION] Opened Google Browser")

def open_paint():
    _run_action("mspaint", fallback_label="Paint")

def open_cmd():
    _run_action("cmd", fallback_label="Command Prompt")

def open_explorer():
    _run_action("explorer", fallback_label="File Explorer")

def open_youtube():
    try:
        webbrowser.open("https://youtube.com")
    except Exception:
        pass
    logging.info("[ACTION] Opened YouTube")

def open_spotify():
    _run_action("spotify", fallback_label="Spotify")

def open_settings():
    _run_action("ms-settings:", fallback_label="Windows Settings")
