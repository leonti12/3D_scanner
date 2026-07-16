from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt

from scanner.core.worker import HardwareWorker
from scanner.hardware.camera import init_camera_stream
from scanner.hardware.motion import trigger_triangulation, toggle_status_led
from scanner.hardware.gpio_io import HARDWARE_AVAILABLE
from scanner.ui.theme import C, PRIMARY_BTN_QSS
from scanner.ui.widgets import top_bar, status_pill


class ControlScreen(QWidget):
    def __init__(self, app_window):
        super().__init__()
        self.app_window = app_window
        self.worker = None
        self.led_state = {"on": False}

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)
        outer.addWidget(top_bar("MANUAL CONTROL", on_back=lambda: self.app_window.go_to("home")))

        body = QVBoxLayout()
        body.setContentsMargins(14, 10, 14, 10)
        body.setSpacing(10)

        self.status_label = QLabel("Idle")
        self.status_label.setStyleSheet(f"font-size: 12px; color: {C['muted']};")
        pill, self.status_dot = status_pill(self.status_label)
        body.addWidget(pill)

        self.btn_cam = QPushButton("  \u25a1   Init IMX296 Stream")
        self.btn_scan = QPushButton("  \u2316   Trigger Triangulation")
        self.btn_led = QPushButton("  \u25c9   Toggle Status LED")
        for b in (self.btn_cam, self.btn_scan, self.btn_led):
            b.setFixedHeight(48)
            b.setStyleSheet(PRIMARY_BTN_QSS)
            body.addWidget(b)

        self.btn_cam.clicked.connect(lambda: self._run(init_camera_stream))
        self.btn_scan.clicked.connect(lambda: self._run(trigger_triangulation))
        self.btn_led.clicked.connect(lambda: self._run(toggle_status_led, self.led_state))

        if not HARDWARE_AVAILABLE:
            note = QLabel("gpiozero unavailable - mock mode")
            note.setStyleSheet(f"color: {C['muted']}; font-size: 10px;")
            note.setAlignment(Qt.AlignmentFlag.AlignCenter)
            body.addWidget(note)

        body.addStretch()
        outer.addLayout(body)

        self.buttons = [self.btn_cam, self.btn_scan, self.btn_led]

    def _run(self, func, *args):
        self.status_dot.setStyleSheet(f"color: {C['control']}; font-size: 10px;")
        self.status_label.setText("Executing...")
        for b in self.buttons:
            b.setEnabled(False)
        self.worker = HardwareWorker(func, *args)
        self.worker.finished.connect(self._on_done)
        self.worker.error.connect(self._on_error)
        self.worker.start()

    def _on_done(self, result):
        self.status_label.setText(result)
        self.status_dot.setStyleSheet(f"color: {C['ok']}; font-size: 10px;")
        for b in self.buttons:
            b.setEnabled(True)

    def _on_error(self, msg):
        self.status_label.setText(f"Error: {msg}")
        self.status_dot.setStyleSheet(f"color: {C['warn']}; font-size: 10px;")
        for b in self.buttons:
            b.setEnabled(True)
