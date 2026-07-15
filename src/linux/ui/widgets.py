from PySide6.QtWidgets import (
    QLabel,
    QPushButton,
    QTableWidget,
    QComboBox,
    QSizePolicy,
    QAbstractItemView,
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

from ui.spinner import SpinnerWidget
from ui.icons import icon
from constants import CANCEL_ICON_COLOR


def create_widgets(window):
    # ────────────────────────────────────────────────────────
    # Title Bar
    # ────────────────────────────────────────────────────────

    window.title_label = QLabel("CypherGate VPN")
    window.title_label.setFont(QFont("monospace", 11))
    window.title_label.setStyleSheet("color: gold; padding: 4px;")
    window.title_label.setSizePolicy(
        QSizePolicy.Expanding,
        QSizePolicy.Preferred,
    )

    window.btn_min = QPushButton("—")
    window.btn_close = QPushButton("✕")

    for btn in (window.btn_min, window.btn_close):
        btn.setFont(QFont("Noto Sans", 12))
        btn.setFixedSize(30, 28)
        btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: gold;
                border: none;
            }

            QPushButton:hover {
                background-color: #333;
            }
        """)

    # ────────────────────────────────────────────────────────
    # Main Heading
    # ────────────────────────────────────────────────────────

    window.heading_label = QLabel("Available VPN Servers")
    window.heading_label.setAlignment(Qt.AlignCenter)
    window.heading_label.setStyleSheet("font-weight: bold; font-size: 18px;")

    # ────────────────────────────────────────────────────────
    # Country Selector
    # ────────────────────────────────────────────────────────

    window.country_dropdown = QComboBox()

    # ────────────────────────────────────────────────────────
    # Server Table
    # ────────────────────────────────────────────────────────

    window.table = QTableWidget()
    window.table.setColumnCount(4)
    window.table.setHorizontalHeaderLabels(["Country", "Ping", "Speed", "Users"])
    window.table.setSelectionBehavior(QAbstractItemView.SelectRows)
    window.table.setSelectionMode(QAbstractItemView.SingleSelection)

    # ────────────────────────────────────────────────────────
    # Buttons
    # ────────────────────────────────────────────────────────

    window.refresh_btn = QPushButton("Refresh")
    window.refresh_btn.setIcon(icon("refresh"))

    window.connect_btn = QPushButton("Connect")
    window.connect_btn.setIcon(icon("lock"))

    window.auto_btn = QPushButton("Auto-Connect Fastest")
    window.auto_btn.setIcon(icon("rocket"))

    window.disconnect_btn = QPushButton("Disconnect")
    window.disconnect_btn.setIcon(icon("lock-open"))

    window.cancel_button = QPushButton("Cancel")
    window.cancel_button.setIcon(icon("cancel", CANCEL_ICON_COLOR))
    window.cancel_button.setObjectName("cancelButton")
    window.cancel_button.setFixedHeight(32)
    window.cancel_button.setSizePolicy(
        QSizePolicy.Fixed,
        QSizePolicy.Fixed,
    )
    window.cancel_button.hide()

    # ────────────────────────────────────────────────────────
    # Status
    # ────────────────────────────────────────────────────────

    window.spinner = SpinnerWidget()
    window.spinner.hide()

    window.status_label = QLabel("Disconnected")
    window.status_label.setAlignment(Qt.AlignCenter)


def connect_signals(window):
    window.btn_min.clicked.connect(window.showMinimized)
    window.btn_close.clicked.connect(window.close)

    window.country_dropdown.currentTextChanged.connect(window.filter_servers)

    window.refresh_btn.clicked.connect(window.refresh_servers)
    window.connect_btn.clicked.connect(window.connect_vpn)
    window.auto_btn.clicked.connect(window.auto_connect_fastest)
    window.disconnect_btn.clicked.connect(window.disconnect_vpn)
    window.cancel_button.clicked.connect(window.cancel_connection)
