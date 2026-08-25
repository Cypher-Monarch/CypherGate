from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QLabel,
    QPushButton,
    QSizePolicy,
    QTableWidget,
)

from ui.icons import icon
from ui.spinner import SpinnerWidget


def create_widgets(window):
    # ────────────────────────────────────────────────────────
    # Title Bar
    # ────────────────────────────────────────────────────────

    window.title_label = QLabel("CypherGate VPN")
    window.title_label.setObjectName("titleLabel")
    window.title_label.setFont(QFont("monospace", 11))
    window.title_label.setStyleSheet("color: gold; padding: 4px;")
    window.title_label.setSizePolicy(
        QSizePolicy.Policy.Expanding,
        QSizePolicy.Policy.Preferred,
    )

    window.btn_min = QPushButton("—")
    window.btn_min.setObjectName("minimizeButton")

    window.btn_close = QPushButton("✕")
    window.btn_close.setObjectName("closeButton")

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
    window.heading_label.setObjectName("headingLabel")
    window.heading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    window.heading_label.setStyleSheet("font-weight: bold; font-size: 18px;")

    # ────────────────────────────────────────────────────────
    # Country Selector
    # ────────────────────────────────────────────────────────

    window.country_dropdown = QComboBox()
    window.country_dropdown.setObjectName("countryDropdown")

    # ────────────────────────────────────────────────────────
    # Server Table
    # ────────────────────────────────────────────────────────

    window.table = QTableWidget()
    window.table.setObjectName("serverTable")
    window.table.setColumnCount(4)
    window.table.setHorizontalHeaderLabels(["Country", "Ping", "Speed", "Users"])
    window.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
    window.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)

    # ────────────────────────────────────────────────────────
    # Buttons
    # ────────────────────────────────────────────────────────

    window.refresh_btn = QPushButton("Refresh")
    window.refresh_btn.setObjectName("refreshButton")
    window.refresh_btn.setIcon(icon("refresh"))

    window.connect_btn = QPushButton("Connect")
    window.connect_btn.setObjectName("connectButton")
    window.connect_btn.setIcon(icon("connect"))

    window.auto_btn = QPushButton("Auto-Connect Fastest")
    window.auto_btn.setObjectName("autoConnectButton")
    window.auto_btn.setIcon(icon("auto_connect"))

    window.disconnect_btn = QPushButton("Disconnect")
    window.disconnect_btn.setObjectName("disconnectButton")
    window.disconnect_btn.setIcon(icon("disconnect"))

    window.cancel_button = QPushButton("Cancel")
    window.cancel_button.setObjectName("cancelButton")
    window.cancel_button.setIcon(icon("cancel"))
    window.cancel_button.setFixedHeight(32)
    window.cancel_button.setSizePolicy(
        QSizePolicy.Policy.Fixed,
        QSizePolicy.Policy.Fixed,
    )
    window.cancel_button.hide()

    # ────────────────────────────────────────────────────────
    # Status
    # ────────────────────────────────────────────────────────

    window.spinner = SpinnerWidget()
    window.spinner.hide()

    window.status_label = QLabel("Disconnected")
    window.status_label.setObjectName("statusLabel")
    window.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)


def connect_signals(window):
    window.btn_min.clicked.connect(window.showMinimized)
    window.btn_close.clicked.connect(window.close)

    window.country_dropdown.currentTextChanged.connect(window.filter_servers)

    window.refresh_btn.clicked.connect(window.refresh_servers)
    window.connect_btn.clicked.connect(window.connect_vpn)
    window.auto_btn.clicked.connect(window.auto_connect_fastest)
    window.disconnect_btn.clicked.connect(window.disconnect_vpn)
    window.cancel_button.clicked.connect(window.cancel_connection)
