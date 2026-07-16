from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt

from scanner.core.worker import HardwareWorker
from scanner.hardware.motion import home_axes, jog, auto_calibrate
from scanner.ui.theme import C, PRIMARY_BTN_QSS, JOG_BTN_QSS, icon_button_style
from scanner.ui.widgets import top_bar, status_pill


class CalibrationScreen(QWidget):
    def __init__(self, app_window):
        super().__init__()
        self.app_window = app_window
        self.step_size = 1.0
        self.worker = None

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)
        outer.addWidget(top_bar("CALIBRATION", on_back=lambda: self.app_window.go_to("home")))

        body = QVBoxLayout()
        body.setContentsMargins(14, 10, 14, 10)
        body.setSpacing(10)

        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet(f"font-size: 12px; color: {C['muted']};")
        pill, self.status_dot = status_pill(self.status_label)
        body.addWidget(pill)

        step_row = QHBoxLayout()
        step_row.setSpacing(6)
        step_label = QLabel("STEP")
        step_label.setStyleSheet(f"font-size: 10px; color: {C['muted']}; font-weight: 600;")
        step_row.addWidget(step_label)
        self.step_buttons = {}
        for step in (0.1, 1.0, 10.0):
            btn = QPushButton(f"{step:g}")
            btn.setFixedHeight(28)
            btn.clicked.connect(lambda _, s=step: self.set_step_size(s))
            step_row.addWidget(btn)
            self.step_buttons[step] = btn
        body.addLayout(step_row)
        self.set_step_size(1.0)

        pad_row = QHBoxLayout()
        pad_row.setSpacing(14)

        xy = QGridLayout()
        xy.setSpacing(6)
        self.btn_y_plus = self._jog_btn("Y+", "Y", 1)
        self.btn_y_minus = self._jog_btn("Y-", "Y", -1)
        self.btn_x_plus = self._jog_btn("X+", "X", 1)
        self.btn_x_minus = self._jog_btn("X-", "X", -1)
        self.btn_home = self._jog_btn("\u2302", None, None)
        self.btn_home.clicked.connect(self.do_home)

        xy.addWidget(self.btn_y_plus, 0, 1)
        xy.addWidget(self.btn_x_minus, 1, 0)
        xy.addWidget(self.btn_home, 1, 1)
        xy.addWidget(self.btn_x_plus, 1, 2)
        xy.addWidget(self.btn_y_minus, 2, 1)
        pad_row.addLayout(xy)

        z_col = QVBoxLayout()
        z_col.setSpacing(6)
        z_label = QLabel("Z")
        z_label.setStyleSheet(f"font-size: 10px; color: {C['muted']}; font-weight: 600;")
        z_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.btn_z_plus = self._jog_btn("Z+", "Z", 1)
        self.btn_z_minus = self._jog_btn("Z-", "Z", -1)
        z_col.addWidget(z_label)
        z_col.addWidget(self.btn_z_plus)
        z_col.addWidget(self.btn_z_minus)
        pad_row.addLayout(z_col)

        body.addLayout(pad_row)

        self.auto_cal_btn = QPushButton("  \u2316   Auto Calibrate")
        self.auto_cal_btn.setFixedHeight(42)
        self.auto_cal_btn.setStyleSheet(PRIMARY_BTN_QSS)
        self.auto_cal_btn.clicked.connect(self.do_auto_calibrate)
        body.addWidget(self.auto_cal_btn)

        body.addStretch()
        outer.addLayout(body)

        self.jog_buttons = [
            self.btn_y_plus, self.btn_y_minus, self.btn_x_plus, self.btn_x_minus,
            self.btn_z_plus, self.btn_z_minus, self.btn_home, self.auto_cal_btn,
        ]

    def _jog_btn(self, label, axis, direction):
        btn = QPushButton(label)
        btn.setFixedSize(50, 50)
        btn.setStyleSheet(JOG_BTN_QSS)
        if axis is not None:
            btn.clicked.connect(lambda: self.do_jog(axis, direction))
        return btn

    def set_step_size(self, step):
        self.step_size = step
        for s, btn in self.step_buttons.items():
            active = s == step
            if active:
                btn.setStyleSheet(icon_button_style(C['calibrate'], border=C['calibrate']) +
                                   f"QPushButton {{ color: #1a1a1a; background-color: {C['calibrate']}; }}")
            else:
                btn.setStyleSheet(icon_button_style(C['calibrate'], border=C['border']))

    def _run(self, func, *args):
        self._set_buttons_enabled(False)
        self.status_dot.setStyleSheet(f"color: {C['calibrate']}; font-size: 10px;")
        self.status_label.setText("Working...")
        self.worker = HardwareWorker(func, *args)
        self.worker.finished.connect(self._on_done)
        self.worker.error.connect(self._on_error)
        self.worker.start()

    def do_jog(self, axis, direction):
        self._run(jog, axis, direction * self.step_size)

    def do_home(self):
        self._run(home_axes)

    def do_auto_calibrate(self):
        self._run(auto_calibrate)

    def _on_done(self, result):
        self.status_label.setText(result)
        self.status_dot.setStyleSheet(f"color: {C['ok']}; font-size: 10px;")
        self._set_buttons_enabled(True)

    def _on_error(self, msg):
        self.status_label.setText(f"Error: {msg}")
        self.status_dot.setStyleSheet(f"color: {C['warn']}; font-size: 10px;")
        self._set_buttons_enabled(True)

    def _set_buttons_enabled(self, enabled):
        for btn in self.jog_buttons:
            btn.setEnabled(enabled)
