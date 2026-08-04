from PySide6.QtCore import Qt
from PySide6.QtWidgets import QSystemTrayIcon

# ────────────────────────────────────────────────────────
# Event Handlers
# ────────────────────────────────────────────────────────


def closeEvent(self, event):
    event.ignore()
    self.hide()
    self.tray_icon.showMessage(
        "CypherGate",
        "App minimized to tray. Double-click to restore.",
        QSystemTrayIcon.MessageIcon.Information,
        2000,
    )


def mousePressEvent(self, event):
    if event.button() == Qt.MouseButton.LeftButton:
        self.drag_pos = event.globalPosition().toPoint()


def mouseMoveEvent(self, event):
    if event.buttons() == Qt.MouseButton.LeftButton:
        self.move(self.pos() + event.globalPosition().toPoint() - self.drag_pos)
        self.drag_pos = event.globalPosition().toPoint()
