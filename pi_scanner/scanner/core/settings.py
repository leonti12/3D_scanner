"""Load/save the scanner's user-adjustable settings as JSON."""

import json
import os

from scanner.core.config import SETTINGS_PATH

DEFAULT_SETTINGS = {
    "laser_power": 70,
    "led_brightness": 100,
    "camera_exposure": 50,
    "auto_home_on_start": False,
    "enable_camera_preview": True,
}


def load_settings():
    if os.path.exists(SETTINGS_PATH):
        try:
            with open(SETTINGS_PATH, "r") as f:
                data = json.load(f)
            merged = DEFAULT_SETTINGS.copy()
            merged.update(data)
            return merged
        except (json.JSONDecodeError, OSError):
            pass
    return DEFAULT_SETTINGS.copy()


def save_settings(settings):
    with open(SETTINGS_PATH, "w") as f:
        json.dump(settings, f, indent=2)
