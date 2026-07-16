"""
Motion, triangulation, and status-LED logic. These are the functions the
UI's worker threads call - keep every real stepper/I2C/SPI call in here so
the UI layer never touches hardware directly.
"""

import time

from scanner.core.config import STATUS_LED_PIN
from scanner.hardware.gpio_io import get_led


def trigger_triangulation():
    """Fire the laser and run one triangulation pass."""
    led = get_led(STATUS_LED_PIN)
    led.on()
    # TODO: real triangulation scan logic (I2C/SPI comms, capture + sensor fusion)
    time.sleep(2)
    led.off()
    return "Triangulation scan complete"


def toggle_status_led(state_holder):
    """state_holder is a small mutable dict so callers can track LED state."""
    led = get_led(STATUS_LED_PIN)
    if state_holder.get("on"):
        led.off()
        state_holder["on"] = False
        return "Status LED OFF"
    led.on()
    state_holder["on"] = True
    return "Status LED ON"


def home_axes():
    """Send a homing command to your stepper/motor controller."""
    # TODO: real homing routine
    time.sleep(1.5)
    return "Axes homed"


def jog(axis, distance_mm):
    """Move a single axis by distance_mm (can be negative)."""
    # TODO: real stepper move
    time.sleep(0.3)
    return f"Jogged {axis} by {distance_mm:+.2f} mm"


def auto_calibrate():
    """Full auto-calibration routine."""
    # TODO: real calibration sequence
    time.sleep(3)
    return "Auto-calibration complete"
