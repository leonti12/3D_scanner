"""Small reusable widgets shared across screens."""

from PyQt6.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt

from scanner.ui.theme import C, icon_button_style


class IconTile(QPushButton):
    """A colour-coded home-screen tile: big glyph + caption, printer-UI style."""

    def __init__(self, glyph, caption, color):
        super().__init__()
        self.setFixedSize(132, 108)
        self.setStyleSheet(icon_button_style(color))

        box = QVBoxLayout(self)
        box.setContentsMargins(4, 8, 4, 8)
        box.setSpacing(4)

        icon = QLabel(glyph)
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon.setStyleSheet(f"font-size: 34px; color: {color}; background: transparent;")
        icon.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        text = QLabel(caption)
        text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        text.setStyleSheet(f"font-size: 12px; font-weight: 600; color: {C['text']}; background: transparent;")
        text.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        box.addStretch()
        box.addWidget(icon)
        box.addWidget(text)
        box.addStretch()


def top_bar(title_text, on_back=None, on_exit=None):
    """Compact 40px-tall header used on every screen."""
    bar = QWidget()
    bar.setFixedHeight(40)
    bar.setStyleSheet(f"background-color: {C['panel']}; border-bottom: 1px solid {C['border']};")
    row = QHBoxLayout(bar)
    row.setContentsMargins(6, 2, 6, 2)

    left = QPushButton("\u2190" if on_back else "")
    left.setFixedSize(32, 32)
    left.setEnabled(bool(on_back))
    if on_back:
        left.setStyleSheet(icon_button_style(C['accent']))
        left.clicked.connect(on_back)
    else:
        left.setStyleSheet("background: transparent; border: none;")
    row.addWidget(left)

    title = QLabel(title_text)
    title.setStyleSheet("font-size: 14px; font-weight: 700; letter-spacing: 1px;")
    title.setAlignment(Qt.AlignmentFlag.AlignCenter)
    row.addWidget(title, stretch=1)

    right = QPushButton("\u2715" if on_exit else "")
    right.setFixedSize(32, 32)
    right.setEnabled(bool(on_exit))
    if on_exit:
        right.setStyleSheet(icon_button_style(C['warn']))
        right.clicked.connect(on_exit)
    else:
        right.setStyleSheet("background: transparent; border: none;")
    row.addWidget(right)

    return bar


def status_pill(text_label):
    """Small status row with a coloured dot + label, used under top bars."""
    wrap = QWidget()
    row = QHBoxLayout(wrap)
    row.setContentsMargins(2, 4, 2, 4)
    row.setSpacing(6)
    dot = QLabel("\u25cf")
    dot.setStyleSheet(f"color: {C['ok']}; font-size: 10px;")
    row.addWidget(dot)
    row.addWidget(text_label)
    row.addStretch()
    return wrap, dot
