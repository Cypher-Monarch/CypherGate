from PySide6.QtCore import Qt


def setup_window(window):
    window.setWindowFlag(Qt.WindowType.FramelessWindowHint)
    window.setWindowTitle("CypherGate")
    window.setGeometry(100, 100, 800, 550)

    window.setStyleSheet("""
        QWidget {
            background-color: #0f0f0f;
            color: #FFD700;
            font-family: 'monospace';
            font-size: 14px;
        }
        QHeaderView::section {
            background-color: #FFD700;
            color: #0f0f0f;
            font-weight: bold;
        }
        QPushButton {
            background-color: #FFD700;
            color: #0f0f0f;
            border: none;
            padding: 6px;
            border-radius: 4px;
        }
        QPushButton:hover {
            background-color: #e6c200;
        }
        QPushButton#cancelButton {
            background-color: #2B2B2B;

            color: #FFD700;

            border: 1px solid #8B7A42;

            border-radius: 16px;

            min-height: 32px;
            padding: 0px 18px;

            font-size: 10pt;
        }

        QPushButton#cancelButton:hover {
            background-color: #343434;
        }

        QPushButton#cancelButton:pressed {
            background-color: #202020;
        }
        QTableWidget::item:selected {
            background-color: #FFD700;
            color: #0f0f0f;
            font-weight: bold;
        }
    """)
