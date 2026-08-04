from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QIcon, QPainter, QPixmap
from PySide6.QtSvg import QSvgRenderer

from constants import ICON_COLOR, ICON_DIR, ICON_SIZE

_ICON_CACHE = {}


def icon(name, color=ICON_COLOR, size=ICON_SIZE):
    key = (name, color, size)

    if key in _ICON_CACHE:
        return _ICON_CACHE[key]

    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)

    renderer = QSvgRenderer(str(Path(ICON_DIR) / f"{name}.svg"))

    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
    painter.fillRect(pixmap.rect(), QColor(color))
    painter.end()

    qicon = QIcon(pixmap)
    _ICON_CACHE[key] = qicon

    return qicon
