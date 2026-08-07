import os
import threading
import time

import requests
from plyer import notification
from PySide6.QtCore import (
    QEasingCurve,
    QPropertyAnimation,
    QRectF,
    Qt,
    QTimer,
    Signal,
)
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QGraphicsOpacityEffect,
    QLabel,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QWidget,
)

from constants import (
    API_URL,
    CACHE_FILE,
    CONNECTION_TIMEOUT,
    ICON_PATH,
    STATUS_POLL_INTERVAL,
)
from ipc import ensure_root_handler, get_status, send_root_command
from permissions import check_permissions
from ui.animations import (
    animated_exit,
    animated_restore,
    final_close,
    final_minimize,
    on_tray_icon_activated,
    start_spinner,
    stop_spinner,
    tray_restore,
)
from ui.events import closeEvent, mouseMoveEvent, mousePressEvent
from ui.layout import setup_layout
from ui.spinner import SpinnerWidget
from ui.status import sync_ui_state
from ui.tray import create_tray
from ui.widgets import connect_signals, create_widgets
from ui.window import setup_window
from update import check_for_updates
from vpn.connector import prepare_connection, write_config
from vpn.loader import filter_servers as filter_server_list
from vpn.loader import parse_server_data

# ────────────────────────────────────────────────────────
# Main Application Class
# ────────────────────────────────────────────────────────


class CypherGate(QWidget):
    data_loaded = Signal(str)

    def __init__(self):
        super().__init__()

        self.data_loaded.connect(self.process_server_data)

        setup_window(self)
        create_widgets(self)
        setup_layout(self)
        connect_signals(self)

        self.ensure_root_handler_async()

        self.spinner.show()
        self.status_label.setText("Fetching servers...")

        self.connect_btn.setEnabled(False)
        self.refresh_btn.setEnabled(False)

        self.load_servers_async()

        self.watch_timer = QTimer(self)
        self.watch_timer.timeout.connect(self.check_vpn_status)
        self.previous_status = None

        self.tray_icon = create_tray(self, ICON_PATH)

        perms = check_permissions()

        if not perms["ok"]:
            self.show_permission_dialog(perms)

        check_for_updates(self)

        sync_ui_state(self, get_status())

    def show_permission_dialog(self, perms):
        dialog = QMessageBox(self)

        dialog.setIcon(QMessageBox.Icon.Warning)
        dialog.setWindowTitle(perms["title"])
        dialog.setText(perms["message"])

        copy_button = None

        if perms.get("copy"):
            copy_button = dialog.addButton(
                "Copy Command",
                QMessageBox.ButtonRole.ActionRole,
            )

        dialog.addButton(QMessageBox.StandardButton.Close)

        dialog.exec()

        if copy_button and dialog.clickedButton() == copy_button:
            QApplication.clipboard().setText(perms["copy"])

    # ────────────────────────────────────────────────────────
    # Core VPN Logic
    # ────────────────────────────────────────────────────────

    def ensure_root_handler_async(self):
        def task():
            ensure_root_handler()

        threading.Thread(target=task, daemon=True).start()

    def load_servers_async(self):
        def task():
            try:
                response = requests.get(API_URL, timeout=30)
                response.raise_for_status()
                data = response.text
                with open(CACHE_FILE, "w", encoding="utf-8") as f:
                    f.write(data)

            except Exception as e:
                if os.path.exists(CACHE_FILE):
                    with open(CACHE_FILE, "r", encoding="utf-8") as f:
                        data = f.read()
                else:
                    error_message = str(e)
                    QTimer.singleShot(
                        0,
                        lambda: QMessageBox.critical(
                            self,
                            "Error",
                            f"Failed to fetch VPN servers and no cache found:\n{error_message}",
                        ),
                    )
                    return

            self.data_loaded.emit(data)

        threading.Thread(target=task, daemon=True).start()

    def filter_servers(self, country):
        self.filtered_servers = filter_server_list(
            self.all_servers,
            country,
        )
        self.populate_table(self.filtered_servers)

    def process_server_data(self, data):
        servers, countries = parse_server_data(data)

        self.all_servers = servers

        self.country_dropdown.clear()
        self.country_dropdown.addItems(countries)

        if countries:
            self.filter_servers(self.country_dropdown.currentText())

        self.spinner.hide()
        self.status_label.setText("Disconnected")

        self.connect_btn.setEnabled(True)
        self.refresh_btn.setEnabled(True)

    def populate_table(self, servers):
        self.table.setRowCount(len(servers))
        self.filtered_servers = servers

        for i, (country, ping, speed, users, _) in enumerate(servers):
            row_data = [country, ping, speed, users]

            for j, text in enumerate(row_data):
                item = QTableWidgetItem(text)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                item.setForeground(QColor("#E5C100"))
                self.table.setItem(i, j, item)

                cell_rect = self.table.visualItemRect(item)
                start_rect = QRectF(
                    cell_rect.center().x() - cell_rect.width() * 0.1,
                    cell_rect.center().y() - cell_rect.height() * 0.1,
                    cell_rect.width() * 0.2,
                    cell_rect.height() * 0.2,
                ).toRect()

                anim_label = QLabel(text, self.table.viewport())
                anim_label.setStyleSheet(
                    "color: #E5C100; font-family: monospace; background: transparent;"
                )
                anim_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                anim_label.setGeometry(start_rect)
                anim_label.show()

                effect = QGraphicsOpacityEffect(anim_label)
                effect.setOpacity(0)
                anim_label.setGraphicsEffect(effect)

                fade_anim = QPropertyAnimation(effect, b"opacity", self)
                fade_anim.setStartValue(0)
                fade_anim.setEndValue(1)
                fade_anim.setDuration(400)
                fade_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

                geo_anim = QPropertyAnimation(anim_label, b"geometry", self)
                geo_anim.setStartValue(start_rect)
                geo_anim.setEndValue(cell_rect)
                geo_anim.setDuration(400)
                geo_anim.setEasingCurve(QEasingCurve.Type.OutBack)

                delay = 100 * i + 50 * j
                QTimer.singleShot(delay, lambda a=fade_anim: a.start())
                QTimer.singleShot(delay, lambda a=geo_anim: a.start())
                QTimer.singleShot(delay + 400, anim_label.deleteLater)

        self.table.resizeColumnsToContents()
        if self.table.rowCount() > 0:
            self.table.selectRow(0)

    def connect_vpn(self):
        selected = self.table.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "No Selection", "Please select a VPN server.")
            return
        self.start_vpn_connection(self.filtered_servers[selected])

    def auto_connect_fastest(self):
        if not self.filtered_servers:
            QMessageBox.warning(
                self, "No Servers", "No servers available to auto-connect."
            )
            return
        self.start_vpn_connection(self.filtered_servers[0])

    def start_vpn_connection(self, server):
        country, ping, speed, users, _ = server

        config, ovpn_path, disable_ipv6 = prepare_connection(server)

        if disable_ipv6:
            self.ensure_root_handler_async()
            send_root_command({"action": "DISABLE_IPV6"})

        write_config(config, ovpn_path)

        try:
            send_root_command(
                {
                    "action": "START_VPN",
                    "config": ovpn_path,
                    "country": country,
                    "ping": ping,
                    "speed": speed,
                    "users": users,
                }
            )

            self.connection_start = time.monotonic()

            sync_ui_state(self, get_status())

            self.watch_timer.start(STATUS_POLL_INTERVAL)

        except Exception as e:
            QMessageBox.critical(self, "Connection Failed", str(e))

    def check_vpn_status(self):
        try:
            status = get_status()

            if status is None:
                return

            sync_ui_state(self, status)

            current_status = status["status"]

            if self.previous_status != "CONNECTED" and current_status == "CONNECTED":
                self.show_connection_info(
                    status["country"],
                    status["ping"],
                    status["speed"],
                    status["users"],
                )

            self.previous_status = current_status

            if current_status in {"CONNECTED", "ERROR", "DISCONNECTED"}:
                self.watch_timer.stop()
                return

            if time.monotonic() - self.connection_start >= CONNECTION_TIMEOUT:
                self.watch_timer.stop()

                self.ensure_root_handler_async()

                send_root_command({"action": "STOP_VPN"})
                send_root_command({"action": "ENABLE_IPV6"})

                new_status = get_status()
                if new_status:
                    sync_ui_state(self, new_status)
                self.previous_status = None

                QMessageBox.warning(
                    self,
                    "Connection Timed Out",
                    f"The VPN server did not respond within {CONNECTION_TIMEOUT} seconds.",
                )

        except Exception:
            pass

    def refresh_servers(self):
        self.spinner.show()
        self.status_label.setText("Refreshing servers...")
        self.connect_btn.setEnabled(False)
        self.refresh_btn.setEnabled(False)
        self.load_servers_async()

    def show_connection_info(self, country, ping, speed, users):
        try:
            ipv4 = requests.get("https://ipinfo.io/ip", timeout=10).text.strip()
        except Exception:
            ipv4 = "Unknown"
        if notification.notify is not None:
            notification.notify(
                title="CypherGate VPN Connected",
                message=f"{country} | New IPv4: {ipv4}",
                app_name="CypherGate",
            )
        msg = (
            f"Connected to {country}\n"
            f"Ping: {ping}\n"
            f"Speed: {speed}\n"
            f"Users: {users}\n"
            f"Your new IPv4: {ipv4}\n"
        )
        QMessageBox.information(self, "VPN Connected", msg)

    def disconnect_vpn(self):
        if hasattr(self, "watch_timer"):
            self.watch_timer.stop()
        self.ensure_root_handler_async()
        send_root_command({"action": "STOP_VPN"})
        send_root_command({"action": "ENABLE_IPV6"})

        sync_ui_state(self, get_status())

        QMessageBox.information(
            self, "VPN Disconnected", "VPN connection has been terminated."
        )

        if notification.notify is not None:
            notification.notify(
                title="CypherGate VPN Disconnected",
                message="VPN connection has been terminated.",
                app_name="CypherGate",
            )
        self.previous_status = None

    def cancel_connection(self):
        if hasattr(self, "watch_timer"):
            self.watch_timer.stop()

        self.ensure_root_handler_async()

        try:
            send_root_command({"action": "STOP_VPN"})
            send_root_command({"action": "ENABLE_IPV6"})
        except Exception as e:
            QMessageBox.warning(self, "Cancel Failed", str(e))
            return

        sync_ui_state(self, get_status())
        self.previous_status = None

    # Type declarations
    spinner: SpinnerWidget
    status_label: QLabel
    connect_btn: QPushButton
    disconnect_btn: QPushButton
    refresh_btn: QPushButton
    cancel_button: QPushButton
    watch_timer: QTimer
    table: QTableWidget
    country_dropdown: QComboBox

    # Event listeners
    closeEvent = closeEvent
    mousePressEvent = mousePressEvent
    mouseMoveEvent = mouseMoveEvent

    # Animation Methods
    animated_exit = animated_exit
    animated_restore = animated_restore
    on_tray_icon_activated = on_tray_icon_activated
    tray_restore = tray_restore
    start_spinner = start_spinner
    stop_spinner = stop_spinner
    final_close = final_close
    final_minimize = final_minimize
