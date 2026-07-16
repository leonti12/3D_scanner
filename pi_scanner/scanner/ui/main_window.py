from PyQt6.QtWidgets import QWidget, QVBoxLayout, QStackedWidget
from PyQt6.QtCore import Qt

from scanner.core.config import SCREEN_W, SCREEN_H, KIOSK_MODE
from scanner.ui.theme import APP_QSS
from scanner.ui.screens.home import HomeScreen
from scanner.ui.screens.calibration import CalibrationScreen
from scanner.ui.screens.settings_screen import SettingsScreen
from scanner.ui.screens.control import ControlScreen
from scanner.ui.screens.info import InfoScreen


class TouchPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PiTouchApp")
        self.setStyleSheet(APP_QSS)

        if KIOSK_MODE:
            self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
            self.showFullScreen()
        else:
            self.setFixedSize(SCREEN_W, SCREEN_H)

        self.setCursor(Qt.CursorShape.BlankCursor)

        self.stack = QStackedWidget()
        self.screens = {
            "home": HomeScreen(self),
            "calibrate": CalibrationScreen(self),
            "settings": SettingsScreen(self),
            "control": ControlScreen(self),
            "info": InfoScreen(self),
        }
        for screen in self.screens.values():
            self.stack.addWidget(screen)

        outer = QVBoxLayout()
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(self.stack)
        self.setLayout(outer)

        self.go_to("home")

    def go_to(self, screen_name):
        self.stack.setCurrentWidget(self.screens[screen_name])

    def keyPressEvent(self, event):
        # Handy during development: Esc to quit even in kiosk mode
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        super().keyPressEvent(event)
