import os
import platform

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame

from scanner.core.config import SETTINGS_PATH
from scanner.hardware.gpio_io import HARDWARE_AVAILABLE
from scanner.ui.theme import C, CARD_QSS
from scanner.ui.widgets import top_bar


class InfoScreen(QWidget):
    def __init__(self, app_window):
        super().__init__()
        self.app_window = app_window

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)
        outer.addWidget(top_bar("INFO", on_back=lambda: self.app_window.go_to("home")))

        body = QVBoxLayout()
        body.setContentsMargins(14, 12, 14, 12)
        body.setSpacing(10)

        rows = [
            ("Platform", f"{platform.system()} {platform.release()}"),
            ("Python", platform.python_version()),
            ("Hardware", "gpiozero (live)" if HARDWARE_AVAILABLE else "mock mode"),
            ("Settings file", os.path.basename(SETTINGS_PATH)),
        ]
        for label_text, value_text in rows:
            frame = QFrame()
            frame.setStyleSheet(CARD_QSS)
            row = QVBoxLayout(frame)
            row.setContentsMargins(12, 8, 12, 8)
            row.setSpacing(2)
            lbl = QLabel(label_text.upper())
            lbl.setStyleSheet(f"font-size: 10px; color: {C['muted']}; font-weight: 600;")
            val = QLabel(value_text)
            val.setStyleSheet("font-size: 13px;")
            val.setWordWrap(True)
            row.addWidget(lbl)
            row.addWidget(val)
            body.addWidget(frame)

        body.addStretch()
        outer.addLayout(body)
