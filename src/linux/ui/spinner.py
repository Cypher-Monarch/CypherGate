from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QTimer, QRectF
from PySide6.QtGui import QPainter, QColor, QPen

# ────────────────────────────────────────────────────────
# Spinner Widget
# ────────────────────────────────────────────────────────


class SpinnerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.angle = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.rotate)
        self.timer.start(16)
        self.setFixedSize(40, 40)

    def rotate(self):
        self.angle = (self.angle + 6) % 360
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()
        center = rect.center()
        radius = min(rect.width(), rect.height()) / 2 - 5
        pen = QPen(QColor("#FFD700"), 3)
        painter.setPen(pen)
        painter.translate(center)
        painter.rotate(self.angle)
        painter.drawArc(QRectF(-radius, -radius, 2 * radius, 2 * radius), 0, 120 * 16)
