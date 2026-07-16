"""Generic background worker so hardware/blocking calls never freeze the UI."""

import logging

from PyQt6.QtCore import QThread, pyqtSignal

logger = logging.getLogger(__name__)


class HardwareWorker(QThread):
    """Runs any callable off the UI thread and reports back via signals."""

    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        try:
            result = self.func(*self.args, **self.kwargs)
            self.finished.emit(str(result))
        except Exception as exc:
            logger.exception("Hardware task failed: %s", self.func.__name__)
            self.error.emit(str(exc))
