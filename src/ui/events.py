from PySide6.QtCore import Qt
from PySide6.QtWidgets import QSystemTrayIcon

# ────────────────────────────────────────────────────────
# Event Handlers
# ────────────────────────────────────────────────────────


def closeEvent(window, event):
    if window.settings["application"]["minimize_to_tray"]:
        event.ignore()
        window.hide()
        window.tray_icon.showMessage(
            "CypherGate",
            "App minimized to tray. Double-click to restore.",
            QSystemTrayIcon.MessageIcon.Information,
            2000,
        )
    else:
        event.accept()


def mousePressEvent(window, event):
    if event.button() == Qt.MouseButton.LeftButton:
        window.drag_pos = event.globalPosition().toPoint()


def mouseMoveEvent(window, event):
    if event.buttons() == Qt.MouseButton.LeftButton:
        window.move(window.pos() + event.globalPosition().toPoint() - window.drag_pos)
        window.drag_pos = event.globalPosition().toPoint()
