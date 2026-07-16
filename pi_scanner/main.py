#!/usr/bin/env python3
"""Entry point. Keep this file thin - all real logic lives under scanner/."""

import logging
import sys

from PyQt6.QtWidgets import QApplication

from scanner.core.config import LOG_PATH
from scanner.ui.main_window import TouchPanel


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler(LOG_PATH),
            logging.StreamHandler(sys.stdout),
        ],
    )


def main():
    setup_logging()
    logging.getLogger(__name__).info("Starting PiTouchApp")

    app = QApplication(sys.argv)
    window = TouchPanel()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
