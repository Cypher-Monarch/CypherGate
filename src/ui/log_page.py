from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QPlainTextEdit, QPushButton, QVBoxLayout, QWidget


def create_logs_page(window):
    page = QWidget()
    page.setObjectName("logsPage")

    layout = QVBoxLayout(page)
    layout.setContentsMargins(12, 18, 12, 12)
    layout.setSpacing(12)

    heading = QLabel("Connection Logs")
    heading.setObjectName("headingLabel")
    heading.setAlignment(Qt.AlignmentFlag.AlignCenter)

    window.logs_status_label = QLabel("No active session log")
    window.logs_status_label.setObjectName("logsStatusLabel")

    window.logs_output = QPlainTextEdit()
    window.logs_output.setObjectName("logsOutput")
    window.logs_output.setReadOnly(True)
    window.logs_output.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
    window.logs_output.setPlaceholderText("Connection logs will appear here.")

    window.logs_copy_btn = QPushButton("Copy Logs")
    window.logs_copy_btn.setObjectName("logsCopyButton")

    back_button = QPushButton("Back")
    back_button.setObjectName("logsBackButton")
    back_button.clicked.connect(window.show_previous_page)

    layout.addWidget(heading)
    layout.addWidget(window.logs_status_label)
    layout.addWidget(window.logs_output, 1)
    layout.addWidget(window.logs_copy_btn)
    layout.addWidget(back_button)

    return page
