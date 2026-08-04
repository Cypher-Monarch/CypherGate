from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
)


def setup_layout(window):
    layout = QVBoxLayout()

    title_bar_layout = QHBoxLayout()
    title_bar_layout.setContentsMargins(0, 0, 0, 0)

    title_bar_layout.addWidget(window.title_label)
    title_bar_layout.addStretch()
    title_bar_layout.addWidget(window.btn_min)
    title_bar_layout.addWidget(window.btn_close)

    title_bar_widget = QWidget()
    title_bar_widget.setLayout(title_bar_layout)

    layout.addWidget(title_bar_widget)

    layout.addWidget(window.heading_label)
    layout.addWidget(window.country_dropdown)
    layout.addWidget(window.table)

    btn_layout = QHBoxLayout()
    btn_layout.addWidget(window.refresh_btn)
    btn_layout.addWidget(window.connect_btn)
    btn_layout.addWidget(window.auto_btn)
    btn_layout.addWidget(window.disconnect_btn)

    layout.addLayout(btn_layout)

    spinner_layout = QHBoxLayout()

    spinner_layout.addWidget(window.spinner, alignment=Qt.AlignmentFlag.AlignCenter)
    spinner_layout.addWidget(
        window.cancel_button, alignment=Qt.AlignmentFlag.AlignCenter
    )

    layout.addLayout(spinner_layout)

    layout.addWidget(window.status_label)

    window.setLayout(layout)
