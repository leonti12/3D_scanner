"""
Central configuration. Nothing hardware- or UI-specific lives elsewhere -
if you're changing a pin number, a screen size, or a path, it's here.
"""

import os

# --- Display -----------------------------------------------------------
SCREEN_W, SCREEN_H = 320, 480

# KIOSK_MODE controls whether the window launches frameless + fullscreen.
# Defaults to True (real device behaviour). Override for desktop dev with:
#   SCANNER_KIOSK=0 python3 main.py
KIOSK_MODE = os.environ.get("SCANNER_KIOSK", "1") != "0"

# --- Hardware ------------------------------------------------------------
STATUS_LED_PIN = 17  # BCM pin - change to your wiring

# --- Paths -----------------------------------------------------------
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SETTINGS_PATH = os.path.join(PROJECT_ROOT, "settings.json")
LOG_PATH = os.path.join(PROJECT_ROOT, "scanner.log")
