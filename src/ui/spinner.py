from typing import Any

from PySide6.QtCore import QRectF, QTimer
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtWidgets import QWidget

from config.manager import load_settings

# ────────────────────────────────────────────────────────
# Spinner Widget
# ────────────────────────────────────────────────────────

_SETTINGS: dict[str, Any] | None = None


def reload() -> dict[str, Any]:
    global _SETTINGS

    _SETTINGS = load_settings()
    assert _SETTINGS is not None
    return _SETTINGS


def get_settings() -> dict[str, Any]:
    if _SETTINGS is None:
        return reload()

    return _SETTINGS


def get_spinner_config():
    settings = get_settings()

    return settings["widgets"]["spinner"]


class SpinnerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        settings = get_spinner_config()

        self.angle = 0

        self.fps = settings["fps"]
        self.rotation_speed = settings["rotation_speed"]

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.rotate)
        self.timer.start(1000 // self.fps)

        self.setFixedSize(
            settings["size"],
            settings["size"],
        )

    def rotate(self):
        self.angle = (self.angle + (self.rotation_speed / self.fps)) % 360
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = self.rect()
        center = rect.center()
        radius = min(rect.width(), rect.height()) / 2 - 5
        settings = get_spinner_config()
        pen = QPen(
            QColor(settings["color"]),
            settings["thickness"],
        )
        painter.setPen(pen)
        painter.translate(center)
        painter.rotate(self.angle)
        painter.drawArc(QRectF(-radius, -radius, 2 * radius, 2 * radius), 0, 120 * 16)

    def reload_config(self):
        settings = get_spinner_config()

        self.fps = settings["fps"]
        self.rotation_speed = settings["rotation_speed"]

        self.timer.setInterval(1000 // self.fps)

        self.setFixedSize(
            settings["size"],
            settings["size"],
        )

        self.update()
