from PySide6.QtCore import Qt

from config.theme import load_theme


def setup_window(window):
    window.setObjectName("mainWindow")

    window.setWindowFlag(Qt.WindowType.FramelessWindowHint)
    window.setWindowTitle("CypherGate")
    window.setGeometry(100, 100, 800, 550)

    window.setStyleSheet(load_theme("default"))
