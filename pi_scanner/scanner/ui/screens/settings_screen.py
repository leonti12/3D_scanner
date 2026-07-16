from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QScrollArea, QSlider, QCheckBox, QFrame, QLabel, QPushButton
)
from PyQt6.QtCore import Qt

from scanner.core.settings import load_settings, save_settings
from scanner.ui.theme import C, PRIMARY_BTN_QSS, CARD_QSS
from scanner.ui.widgets import top_bar


class SettingsScreen(QWidget):
    def __init__(self, app_window):
        super().__init__()
        self.app_window = app_window
        self.settings = load_settings()

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)
        outer.addWidget(top_bar("SETTINGS", on_back=self.on_back))

        body = QVBoxLayout()
        body.setContentsMargins(12, 10, 12, 10)
        body.setSpacing(8)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setSpacing(10)
        content_layout.setContentsMargins(2, 2, 2, 2)

        self.sliders = {}
        content_layout.addWidget(self._slider_row("Laser power", "laser_power", 0, 100, C['calibrate']))
        content_layout.addWidget(self._slider_row("LED brightness", "led_brightness", 0, 100, C['control']))
        content_layout.addWidget(self._slider_row("Camera exposure", "camera_exposure", 0, 100, C['info']))

        self.checkboxes = {}
        content_layout.addWidget(self._toggle_row("Auto-home on startup", "auto_home_on_start"))
        content_layout.addWidget(self._toggle_row("Enable camera preview", "enable_camera_preview"))

        content_layout.addStretch()
        scroll.setWidget(content)
        body.addWidget(scroll, stretch=1)

        save_btn = QPushButton("  \u2713   Save Settings")
        save_btn.setFixedHeight(40)
        save_btn.setStyleSheet(PRIMARY_BTN_QSS)
        save_btn.clicked.connect(self.save)
        body.addWidget(save_btn)

        self.save_status = QLabel("")
        self.save_status.setStyleSheet(f"color: {C['muted']}; font-size: 11px;")
        self.save_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        body.addWidget(self.save_status)

        outer.addLayout(body)

    def _card(self):
        frame = QFrame()
        frame.setStyleSheet(CARD_QSS)
        return frame

    def _slider_row(self, label_text, key, lo, hi, accent):
        frame = self._card()
        row = QVBoxLayout(frame)
        row.setContentsMargins(12, 8, 12, 8)
        row.setSpacing(4)

        top = QHBoxLayout()
        label = QLabel(label_text)
        label.setStyleSheet("font-size: 12px;")
        value_label = QLabel(str(self.settings[key]))
        value_label.setStyleSheet(f"color: {accent}; font-weight: bold; font-size: 12px;")
        top.addWidget(label)
        top.addStretch()
        top.addWidget(value_label)
        row.addLayout(top)

        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setRange(lo, hi)
        slider.setValue(self.settings[key])
        slider.setFixedHeight(26)
        slider.valueChanged.connect(lambda v, k=key, lbl=value_label: self._on_slider_changed(k, v, lbl))
        row.addWidget(slider)

        self.sliders[key] = slider
        return frame

    def _toggle_row(self, label_text, key):
        frame = self._card()
        row = QHBoxLayout(frame)
        row.setContentsMargins(12, 10, 12, 10)

        label = QLabel(label_text)
        label.setStyleSheet("font-size: 12px;")
        checkbox = QCheckBox()
        checkbox.setChecked(self.settings[key])
        checkbox.stateChanged.connect(lambda state, k=key: self._on_toggle_changed(k, state))

        row.addWidget(label)
        row.addStretch()
        row.addWidget(checkbox)

        self.checkboxes[key] = checkbox
        return frame

    def _on_slider_changed(self, key, value, value_label):
        self.settings[key] = value
        value_label.setText(str(value))

    def _on_toggle_changed(self, key, state):
        self.settings[key] = bool(state)

    def save(self):
        save_settings(self.settings)
        self.save_status.setText("Saved.")

    def on_back(self):
        self.app_window.go_to("home")
