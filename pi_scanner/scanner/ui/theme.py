"""Shared colours and stylesheets so every screen looks consistent."""

C = {
    "bg": "#14161a",
    "panel": "#1e2128",
    "panel_hi": "#262a33",
    "border": "#31353f",
    "text": "#eef0f3",
    "muted": "#7d8494",
    "accent": "#12b3ac",
    "accent_dark": "#0d8781",
    "warn": "#e63946",
    "ok": "#3ecf6e",
    "control": "#12b3ac",
    "calibrate": "#f2a541",
    "settings": "#8a6fdf",
    "info": "#4a90c4",
}

APP_QSS = f"""
QWidget {{ background-color: {C['bg']}; color: {C['text']}; font-family: 'DejaVu Sans', Arial; }}
QLabel {{ background: transparent; }}
QScrollArea {{ border: none; background: transparent; }}
QScrollBar:vertical {{ width: 8px; background: {C['bg']}; }}
QScrollBar::handle:vertical {{ background: {C['border']}; border-radius: 4px; min-height: 20px; }}
QSlider::groove:horizontal {{ height: 6px; background: {C['border']}; border-radius: 3px; }}
QSlider::handle:horizontal {{
    width: 20px; height: 20px; margin: -7px 0; border-radius: 10px;
    background: {C['accent']};
}}
QSlider::sub-page:horizontal {{ background: {C['accent']}; border-radius: 3px; }}
QCheckBox::indicator {{ width: 24px; height: 24px; border-radius: 6px; border: 2px solid {C['border']}; background: {C['panel_hi']}; }}
QCheckBox::indicator:checked {{ background: {C['accent']}; border-color: {C['accent']}; }}
"""


def icon_button_style(bg, border=None):
    return f"""
    QPushButton {{
        background-color: {C['panel']};
        border: 2px solid {border or C['border']};
        border-radius: 10px;
        color: {C['text']};
    }}
    QPushButton:pressed {{ background-color: {C['panel_hi']}; border-color: {bg}; }}
    QPushButton:disabled {{ color: {C['muted']}; border-color: {C['border']}; }}
    """


PRIMARY_BTN_QSS = f"""
QPushButton {{
    font-size: 13px; font-weight: 600; padding: 10px; border-radius: 8px;
    background-color: {C['panel']}; border: 1px solid {C['border']};
    color: {C['text']}; text-align: left; padding-left: 14px;
}}
QPushButton:pressed {{ background-color: {C['accent_dark']}; }}
QPushButton:disabled {{ color: {C['muted']}; }}
"""

JOG_BTN_QSS = f"""
QPushButton {{
    font-size: 16px; font-weight: bold; border-radius: 8px;
    background-color: {C['panel']}; border: 1px solid {C['border']}; color: {C['text']};
}}
QPushButton:pressed {{ background-color: {C['calibrate']}; color: #1a1a1a; }}
QPushButton:disabled {{ color: {C['muted']}; }}
"""

CARD_QSS = f"background-color: {C['panel']}; border: 1px solid {C['border']}; border-radius: 8px;"
