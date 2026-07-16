"""
Camera control for the IMX296 (or whichever sensor you're on).

Two real options on a Pi:
  1. picamera2 (the modern Python library) - lower latency, more control.
  2. libcamera-still / rpicam-still via shell.run_command - simpler, good
     enough if you just need still captures for triangulation.

This starts with the shell-command approach since it needs zero extra
Python dependencies to try; swap in picamera2 calls here once you've
picked your capture pipeline, everything else in the app is unaffected.
"""

import logging
import time

from scanner.hardware.shell import run_command, ShellError

logger = logging.getLogger(__name__)


def init_camera_stream():
    """
    Starts/validates the camera stream.
    Placeholder using rpicam-hello to confirm the sensor responds; replace
    with your actual picamera2 Picamera2().start() call if you go that route.
    """
    try:
        run_command(["rpicam-hello", "--timeout", "500", "--nopreview"], timeout=10)
        return "Camera stream initialized"
    except ShellError as exc:
        # Simulated fallback so the UI is still testable off the real sensor.
        logger.warning("Camera command unavailable (%s), simulating.", exc)
        time.sleep(1)
        return "Camera stream initialized (simulated)"


def capture_still(output_path):
    """Capture a single frame to output_path."""
    run_command(["rpicam-still", "-o", output_path, "-t", "1000", "--nopreview"], timeout=15)
    return output_path
