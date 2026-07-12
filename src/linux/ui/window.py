from PySide6.QtCore import Qt


def setup_window(window):
    window.setWindowFlag(Qt.FramelessWindowHint)
    window.setWindowTitle("CypherGate")
    window.setGeometry(100, 100, 800, 550)

    window.setStyleSheet("""
        QWidget {
            background-color: #000000;
            color: #FFD700;
            font-family: 'monospace';
            font-size: 14px;
        }
        QHeaderView::section {
            background-color: #FFD700;
            color: #000000;
            font-weight: bold;
        }
        QPushButton {
            background-color: #FFD700;
            color: #000000;
            border: none;
            padding: 6px;
            border-radius: 4px;
        }
        QPushButton:hover {
            background-color: #e6c200;
        }
        QTableWidget::item:selected {
            background-color: #FFD700;
            color: #000000;
            font-weight: bold;
        }
    """)
