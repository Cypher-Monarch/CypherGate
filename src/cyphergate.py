import sys

from PySide6.QtCore import QTimer
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from ui.main_window import CypherGate

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("Assets/icon.png"))
    window = CypherGate()
    window.show()

    # Center the window
    frame = window.frameGeometry()
    center_point = QApplication.primaryScreen().availableGeometry().center()
    frame.moveCenter(center_point)
    window.move(frame.topLeft())

    # Save geometry after it's fully drawn
    QTimer.singleShot(
        0, lambda: setattr(window, "original_geometry", window.geometry())
    )

    sys.exit(app.exec())
