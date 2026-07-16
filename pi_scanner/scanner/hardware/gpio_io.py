"""
GPIO access, isolated behind this module so the rest of the app never
imports gpiozero directly. Falls back to a console-logging mock when
gpiozero (or the actual hardware) isn't available, so the UI still runs
on a dev laptop.
"""

import logging

logger = logging.getLogger(__name__)

try:
    from gpiozero import LED as _LED
    HARDWARE_AVAILABLE = True
except (ImportError, Exception):
    HARDWARE_AVAILABLE = False

    class _LED:  # mock
        def __init__(self, pin):
            self.pin = pin
            self._state = False

        def on(self):
            self._state = True
            logger.info("[MOCK] LED(pin=%s) ON", self.pin)

        def off(self):
            self._state = False
            logger.info("[MOCK] LED(pin=%s) OFF", self.pin)

        def toggle(self):
            self._state = not self._state
            logger.info("[MOCK] LED(pin=%s) %s", self.pin, "ON" if self._state else "OFF")


# Reuse one LED object per pin instead of constructing a new one on every
# call (the bug in the very first draft of this app: a fresh LED() per
# call, or worse, one shared as a class attribute across instances).
_led_cache = {}


def get_led(pin):
    if pin not in _led_cache:
        _led_cache[pin] = _LED(pin)
    return _led_cache[pin]
