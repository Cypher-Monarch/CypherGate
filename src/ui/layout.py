from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from ui.dashboard import create_dashboard
from ui.log_page import create_logs_page


def setup_layout(window):
    layout = QVBoxLayout()

    title_bar_layout = QHBoxLayout()
    title_bar_layout.setContentsMargins(0, 0, 0, 0)

    title_bar_layout.addWidget(window.title_label)
    title_bar_layout.addStretch()
    title_bar_layout.addWidget(window.btn_min)
    title_bar_layout.addWidget(window.btn_close)

    title_bar_widget = QWidget()
    title_bar_widget.setObjectName("titleBar")
    title_bar_widget.setLayout(title_bar_layout)
    layout.addWidget(title_bar_widget)

    # Page 1: Existing server-selection interface
    window.server_page = QWidget()
    server_layout = QVBoxLayout(window.server_page)
    server_layout.setContentsMargins(0, 0, 0, 0)
    server_layout.addWidget(window.heading_label)
    server_layout.addWidget(window.country_dropdown)
    server_layout.addWidget(window.table)

    btn_layout = QHBoxLayout()
    btn_layout.addWidget(window.refresh_btn)
    btn_layout.addWidget(window.connect_btn)
    btn_layout.addWidget(window.auto_btn)
    btn_layout.addWidget(window.disconnect_btn)
    server_layout.addLayout(btn_layout)

    spinner_layout = QHBoxLayout()
    spinner_layout.addWidget(window.spinner, alignment=Qt.AlignmentFlag.AlignCenter)
    spinner_layout.addWidget(
        window.cancel_button, alignment=Qt.AlignmentFlag.AlignCenter
    )
    server_layout.addLayout(spinner_layout)
    status_actions = QHBoxLayout()
    status_actions.addWidget(window.status_label, 1)
    window.error_logs_btn = QPushButton("View Logs")
    window.error_logs_btn.setObjectName("refreshButton")
    window.error_logs_btn.hide()
    status_actions.addWidget(window.error_logs_btn)
    server_layout.addLayout(status_actions)

    # Pages 2 and 3
    window.dashboard_page = create_dashboard(window)
    window.logs_page = create_logs_page(window)

    window.pages = QStackedWidget()
    window.pages.setObjectName("mainPages")
    window.pages.addWidget(window.server_page)
    window.pages.addWidget(window.dashboard_page)
    window.pages.addWidget(window.logs_page)
    window.pages.setCurrentWidget(window.server_page)

    layout.addWidget(window.pages)
    window.setLayout(layout)
