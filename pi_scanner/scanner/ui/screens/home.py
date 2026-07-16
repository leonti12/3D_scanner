from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel

from scanner.ui.theme import C
from scanner.ui.widgets import top_bar, status_pill, IconTile


class HomeScreen(QWidget):
    def __init__(self, app_window):
        super().__init__()
        self.app_window = app_window
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)
        outer.addWidget(top_bar("3D SCANNER", on_exit=self.app_window.close))

        body = QVBoxLayout()
        body.setContentsMargins(14, 14, 14, 14)
        body.setSpacing(10)

        self.status_label = QLabel("Idle")
        self.status_label.setStyleSheet(f"font-size: 12px; color: {C['muted']};")
        pill, self.status_dot = status_pill(self.status_label)
        body.addWidget(pill)

        grid = QGridLayout()
        grid.setSpacing(12)
        tiles = [
            ("\u2699", "CONTROL", C['control'], "control"),
            ("\u2316", "CALIBRATE", C['calibrate'], "calibrate"),
            ("\u2630", "SETTINGS", C['settings'], "settings"),
            ("\u2139", "INFO", C['info'], "info"),
        ]
        for i, (glyph, caption, color, screen) in enumerate(tiles):
            tile = IconTile(glyph, caption, color)
            tile.clicked.connect(lambda _, s=screen: self.app_window.go_to(s))
            grid.addWidget(tile, i // 2, i % 2)

        body.addLayout(grid)
        body.addStretch()
        outer.addLayout(body)
