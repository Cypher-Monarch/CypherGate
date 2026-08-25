from pathlib import Path
from typing import Any

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QIcon, QPainter, QPixmap
from PySide6.QtSvg import QSvgRenderer

from config.manager import load_settings
from constants import ICON_DIR

_ICON_CACHE: dict[tuple[str, str, int], QIcon] = {}

_SETTINGS: dict[str, Any] | None = None


def reload() -> dict[str, Any]:
    global _SETTINGS

    _SETTINGS = load_settings()
    _ICON_CACHE.clear()

    assert _SETTINGS is not None

    return _SETTINGS


def get_settings() -> dict[str, Any]:
    if _SETTINGS is None:
        reload()

    assert _SETTINGS is not None

    return _SETTINGS


def get_icon_config(name, context="default"):
    settings = get_settings()

    if context == "systray":
        return {
            "color": settings["icons"]["color"]["tray"][name],
            "size": settings["icons"]["size"]["tray"][name],
        }

    return {
        "color": settings["icons"]["color"][name],
        "size": settings["icons"]["size"][name],
    }


def icon(name, context="default"):
    config = get_icon_config(name, context)

    color = config["color"]
    size = config["size"]

    key = (name, color, size)

    if key in _ICON_CACHE:
        return _ICON_CACHE[key]

    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)

    renderer = QSvgRenderer(str(Path(ICON_DIR) / f"{name}.svg"))

    painter = QPainter(pixmap)
    renderer.render(painter)

    painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)

    painter.fillRect(
        pixmap.rect(),
        QColor(color),
    )

    painter.end()

    qicon = QIcon(pixmap)

    _ICON_CACHE[key] = qicon

    return qicon


def apply_icons(window):
    window.refresh_btn.setIcon(icon("refresh"))
    window.connect_btn.setIcon(icon("connect"))
    window.auto_btn.setIcon(icon("auto_connect"))
    window.disconnect_btn.setIcon(icon("disconnect"))
    window.cancel_button.setIcon(icon("cancel"))
