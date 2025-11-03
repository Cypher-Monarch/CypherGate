# ────────────────────────────────────────────────────────
# Imports & Constants
# ────────────────────────────────────────────────────────

import os
import sys
import subprocess
import requests
import csv
import base64
from plyer import notification
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLabel, QMessageBox, QHBoxLayout, QComboBox, QSystemTrayIcon,
    QMenu, QSizePolicy, QGraphicsOpacityEffect
)
from PySide6.QtGui import QIcon, QAction, QFont, QPainter, QColor, QPen
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer, QRectF, QSize, QEvent
import time
import re
from datetime import datetime

API_URL = "http://www.vpngate.net/api/iphone/"
VPN_ROOT=os.path.expanduser("~/.config/cyphergate")
VPN_DIR = os.path.expanduser(f"{VPN_ROOT}/servers")
LOGS_DIR = os.path.join(VPN_ROOT, "logs")
CACHE_FILE = os.path.join(f"{VPN_ROOT}/cache", "serverlist.csv")
COUNTRIES_CONF = os.path.join(f"{VPN_ROOT}","countries.conf")
os.makedirs(VPN_DIR, exist_ok=True)
os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
os.makedirs(os.path.dirname(COUNTRIES_CONF), exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

if not os.path.exists(COUNTRIES_CONF):
    with open(COUNTRIES_CONF, "w") as f:
        f.write("# Example:\nJapan\nUnited States\nIndia\nGermany")

if getattr(sys, 'frozen', False):
    APP_DIR = os.path.dirname(sys.executable)
else:
    APP_DIR = os.path.dirname(os.path.abspath(__file__))

ICON_PATH = os.path.join(APP_DIR,"Assets","icon.png")

VERSION = "1.0.1"

# ────────────────────────────────────────────────────────
# Spinner Widget
# ────────────────────────────────────────────────────────

class SpinnerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.angle = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.rotate)
        self.timer.start(16)
        self.setFixedSize(40, 40)

    def rotate(self):
        self.angle = (self.angle + 6) % 360
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()
        center = rect.center()
        radius = min(rect.width(), rect.height()) / 2 - 5
        pen = QPen(QColor("#FFD700"), 3)
        painter.setPen(pen)
        painter.translate(center)
        painter.rotate(self.angle)
        painter.drawArc(QRectF(-radius, -radius, 2*radius, 2*radius), 0, 120 * 16)

# ────────────────────────────────────────────────────────
# Main Application Class
# ────────────────────────────────────────────────────────

class CypherGate(QWidget):
    def __init__(self):
        super().__init__()

#────────────────────────────────────────────────────────
#Initialization (Components and ui)
#────────────────────────────────────────────────────────

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowTitle("CypherGate")
        self.setGeometry(100, 100, 800, 550)
        self.vpn_process = None

        self.setStyleSheet("""
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

        layout = QVBoxLayout()

        title_bar_layout = QHBoxLayout()
        title_bar_layout.setContentsMargins(0, 0, 0, 0)

        title = QLabel("🌐 CypherGate VPN")
        title.setFont(QFont("monospace", 11))
        title.setStyleSheet("color: gold; padding: 4px;")
        title.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        btn_min = QPushButton("—")
        btn_close = QPushButton("✕")
        for btn in (btn_min, btn_close):
            btn.setFont(QFont("noto sans", 12))
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

        btn_min.clicked.connect(self.showMinimized)
        btn_close.clicked.connect(self.close)

        title_bar_layout.addWidget(title)
        title_bar_layout.addStretch()
        title_bar_layout.addWidget(btn_min)
        title_bar_layout.addWidget(btn_close)

        # Wrap the layout inside a QWidget
        title_bar_widget = QWidget()
        title_bar_widget.setStyleSheet("background-color: black;")
        title_bar_widget.setLayout(title_bar_layout)

        layout.addWidget(title_bar_widget)

        title = QLabel("Available VPN Servers")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-weight: bold; font-size: 18px;")
        layout.addWidget(title)

        self.country_dropdown = QComboBox()
        self.country_dropdown.currentTextChanged.connect(self.filter_servers)
        layout.addWidget(self.country_dropdown)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Country", "Ping", "Speed", "Users"])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        layout.addWidget(self.table)

        btn_layout = QHBoxLayout()
        self.refresh_btn = QPushButton("🔄 Refresh")
        self.refresh_btn.clicked.connect(self.load_servers)
        btn_layout.addWidget(self.refresh_btn)

        self.connect_btn = QPushButton("🔗 Connect")
        self.connect_btn.clicked.connect(self.connect_vpn)
        btn_layout.addWidget(self.connect_btn)

        self.auto_btn = QPushButton("🚀 Auto-Connect Fastest")
        self.auto_btn.clicked.connect(self.auto_connect_fastest)
        btn_layout.addWidget(self.auto_btn)

        self.disconnect_btn = QPushButton("❌ Disconnect")
        self.disconnect_btn.clicked.connect(self.disconnect_vpn)
        self.disconnect_btn.setEnabled(False)
        btn_layout.addWidget(self.disconnect_btn)

        layout.addLayout(btn_layout)

        self.spinner = SpinnerWidget()
        self.spinner.hide()
        layout.addWidget(self.spinner, alignment=Qt.AlignCenter)

        self.status_label = QLabel("🔓 Disconnected")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)

        self.setLayout(layout)
        self.load_servers()

        self.tray_icon = QSystemTrayIcon(QIcon(ICON_PATH), self)
        self.tray_icon.setToolTip("🌐 CypherGate VPN")

        # Tray menu setup
        self.tray_menu = QMenu()

        show_action = QAction("👁️ Show", self)
        show_action.triggered.connect(self.show)
        self.tray_menu.addAction(show_action)

        connect_action = QAction("🔗 Connect", self)
        connect_action.triggered.connect(self.connect_vpn)
        self.tray_menu.addAction(connect_action)

        disconnect_action = QAction("❌ Disconnect", self)
        disconnect_action.triggered.connect(self.disconnect_vpn)
        self.tray_menu.addAction(disconnect_action)

        exit_action = QAction("🚪 Exit", self)
        exit_action.triggered.connect(QApplication.quit)
        self.tray_menu.addAction(exit_action)

        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.activated.connect(self.on_tray_icon_activated)
        self.tray_icon.show()
        self.check_for_updates()

#────────────────────────────────────────────────────────
# Core VPN Logic
#────────────────────────────────────────────────────────

    def load_allowed_countries(self):
        if os.path.exists(COUNTRIES_CONF):
            with open(COUNTRIES_CONF, "r", encoding="utf-8") as f:
                return [line.strip() for line in f if line.strip()]
        return None  # No filter if config missing

    def load_servers(self):
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
                QMessageBox.warning(self, "Offline Mode", "Failed to fetch VPN servers online. Loaded from cache.")
            else:
                QMessageBox.critical(self, "Error", f"Failed to fetch VPN servers and no cache found:\n{e}")
                return

        lines = data.splitlines()[2:]
        reader = csv.reader(lines)
        servers = []
        countries = set()

        allowed_countries = self.load_allowed_countries()

        for row in reader:
            if len(row) < 15:
                continue
            country = row[5]
            if allowed_countries and country not in allowed_countries:
                continue  # Skip this country if not allowed

            ping = row[3] + " ms"
            speed = str(int(int(row[4]) / 1000)) + " kbps"
            users = row[2]
            config_b64 = row[-1]
            servers.append((country, ping, speed, users, config_b64))
            countries.add(country)

        self.all_servers = servers
        self.country_dropdown.clear()
        self.country_dropdown.addItems(sorted(countries))
        if countries:
            self.filter_servers(self.country_dropdown.currentText())

    def filter_servers(self, country):
        filtered = [s for s in self.all_servers if s[0] == country]

        def parse_ping(ping_str):
            try:
                return int(ping_str.split()[0])
            except ValueError:
                return float('inf')

        filtered.sort(key=lambda s: parse_ping(s[1]))
        self.populate_table(filtered)

    def populate_table(self, servers):
        self.table.setRowCount(len(servers))
        self.filtered_servers = servers

        for i, (country, ping, speed, users, _) in enumerate(servers):
            row_data = [country, ping, speed, users]

            for j, text in enumerate(row_data):
                item = QTableWidgetItem(text)
                item.setTextAlignment(Qt.AlignCenter)
                item.setForeground(QColor("#E5C100"))
                self.table.setItem(i, j, item)

                cell_rect = self.table.visualItemRect(item)
                start_rect = QRectF(
                    cell_rect.center().x() - cell_rect.width() * 0.1,
                    cell_rect.center().y() - cell_rect.height() * 0.1,
                    cell_rect.width() * 0.2,
                    cell_rect.height() * 0.2
                ).toRect()

                anim_label = QLabel(text, self.table.viewport())
                anim_label.setStyleSheet("color: #E5C100; font-family: monospace; background: transparent;")
                anim_label.setAlignment(Qt.AlignCenter)
                anim_label.setGeometry(start_rect)
                anim_label.show()

                effect = QGraphicsOpacityEffect(anim_label)
                effect.setOpacity(0)
                anim_label.setGraphicsEffect(effect)

                fade_anim = QPropertyAnimation(effect, b"opacity", self)
                fade_anim.setStartValue(0)
                fade_anim.setEndValue(1)
                fade_anim.setDuration(400)
                fade_anim.setEasingCurve(QEasingCurve.OutCubic)

                geo_anim = QPropertyAnimation(anim_label, b"geometry", self)
                geo_anim.setStartValue(start_rect)
                geo_anim.setEndValue(cell_rect)
                geo_anim.setDuration(400)
                geo_anim.setEasingCurve(QEasingCurve.OutBack)

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
            QMessageBox.warning(self, "No Servers", "No servers available to auto-connect.")
            return
        self.start_vpn_connection(self.filtered_servers[0])

    def start_vpn_connection(self, server):
        def extract_remote_host(config):
            match = re.search(r'^remote\s+([^\s]+)', config, re.MULTILINE)
            return match.group(1) if match else None

        def server_supports_ipv6(host):
            try:
                result = subprocess.run(
                    ["dig", "AAAA", host, "+short"],
                    capture_output=True, text=True
                )
                return bool(result.stdout.strip())
            except:
                return False

        country, ping, speed, users, config_b64 = server
        ovpn_path = os.path.join(VPN_DIR, f"{country}.ovpn")

        config = base64.b64decode(config_b64).decode(errors='ignore')

        # Inject cipher settings if missing
        if "data-ciphers" not in config:
            config += "\ndata-ciphers AES-256-GCM:AES-128-GCM:CHACHA20-POLY1305:AES-128-CBC\n"
        if "cipher" not in config:
            config += "\ncipher AES-128-CBC\n"

        # IPv6 logic
        host = extract_remote_host(config)
        if host and server_supports_ipv6(host):
            if "tun-ipv6" not in config:
                config += "\n".join([
                    "\n", "tun-ipv6",
                    "push-peer-info",
                    "redirect-gateway def1 ipv6",
                    "route-ipv6 2000::/3 ::1"
                ]) + "\n"
        else:
            # Disable IPv6 temporarily using pkexec
            subprocess.Popen(
                ["pkexec", "sysctl", "-w", "net.ipv6.conf.all.disable_ipv6=1"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

        # Save the updated config
        with open(ovpn_path, "w") as f:
            f.write(config)

        try:
            self.log_file = os.path.join(LOGS_DIR, f"cyphergate_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt")
            self.log_file_handle = open(self.log_file, "w")
            self.log_file_handle.write(f"\n\n===== VPN Session Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} =====\n")
            self.vpn_process = subprocess.Popen(
                ["pkexec", "openvpn", "--config", ovpn_path],
                stdout=self.log_file_handle,
                stderr=self.log_file_handle,
            )

            self.start_spinner()
            QApplication.processEvents()
            start = time.time()
            while time.time() - start < 15:
                QApplication.processEvents()
            self.stop_spinner(f"🔒 Connected to {country}")

            self.status_label.setText(f"🔒 Connected to {country}")
            self.connect_btn.setEnabled(False)
            self.disconnect_btn.setEnabled(True)
            self.show_connection_info(country, ping, speed, users)

        except Exception as e:
            QMessageBox.critical(self, "Connection Failed", str(e))
        
        finally: 
            if self.log_file_handle and not self.log_file_handle.closed:
                self.log_file_handle.close()

    def show_connection_info(self, country, ping, speed, users):
        try:
            ipv4 = requests.get("https://ipinfo.io/ip", timeout=10).text.strip()
            ipv6 = requests.get("https://api64.ipify.org", timeout=10).text.strip()
        except:
            ipv4 = "Unknown"
            ipv6 = "Unknown"
        notification.notify(
            title="CypherGate VPN Connected",
            message=f"{country} | New IPv4: {ipv4}",
            app_name="CypherGate"
        )
        msg = (f"🌐 Connected to {country}\n"
               f"🏓 Ping: {ping}\n"
               f"🚀 Speed: {speed}\n"
               f"👥 Users: {users}\n"
               f"🔑 Your new IPv4: {ipv4}\n"
               f"🔑 Your new IPv6: {ipv6}")
        QMessageBox.information(self, "VPN Connected", msg)

    def disconnect_vpn(self):
        if self.vpn_process:
            subprocess.run(["pkexec", "kill", str(self.vpn_process.pid)])
            self.vpn_process = None

            self.status_label.setText("🔓 Disconnected")
            self.connect_btn.setEnabled(True)
            self.disconnect_btn.setEnabled(False)

            if self.log_file_handle and not self.log_file_handle.closed:
                self.log_file_handle.close()

            # Re-enable IPv6 using pkexec
            subprocess.Popen(
                ["pkexec", "sysctl", "-w", "net.ipv6.conf.all.disable_ipv6=0"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            QMessageBox.information(self, "VPN Disconnected", "VPN connection has been terminated.")

            notification.notify(
                title="CypherGate VPN Disconnected",
                message="VPN connection has been terminated.",
                app_name="CypherGate"
            )
#────────────────────────────────────────────────────────
# Update Check
#────────────────────────────────────────────────────────

    def check_for_updates(self):
        try:
            response = requests.get("https://raw.githubusercontent.com/Cypher-Monarch/CypherGate/main/Versions/linux_version.txt", timeout=5)
            latest_version = response.text.strip()
            if latest_version != VERSION:
                QMessageBox.information(
                    self, "Update Available",
                    f"A new version {latest_version} is available! Please update for the latest features and fixes."
                )
        except requests.RequestException as e:
            QMessageBox.warning(
                self, "Update Check Failed",
                f"Could not check for updates: {e}\nYou can manually check on GitHub."
            )

#────────────────────────────────────────────────────────
# Event Handlers
#────────────────────────────────────────────────────────    

    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.tray_icon.showMessage(
            "CypherGate",
            "App minimized to tray. Double-click to restore.",
            QSystemTrayIcon.Information,
            2000
        )
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.globalPosition().toPoint() - self.drag_pos)
            self.drag_pos = event.globalPosition().toPoint()

    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.show()

#────────────────────────────────────────────────────────
# Animation Methods
#────────────────────────────────────────────────────────

    def animated_exit(self, action="close"):
        self.effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.effect)

        self.fade = QPropertyAnimation(self.effect, b"opacity")
        self.fade.setDuration(300)
        self.fade.setStartValue(1)
        self.fade.setEndValue(0)
        self.fade.setEasingCurve(QEasingCurve.InOutQuad)

        if action == "minimize":
            self.geo = self.geometry()
            self.shrink = QPropertyAnimation(self, b"geometry")
            self.shrink.setDuration(300)
            self.shrink.setStartValue(self.geo)
            self.shrink.setEndValue(QRectF(self.geo.center(), QSize(1, 1)).toRect())
            self.shrink.setEasingCurve(QEasingCurve.InOutCubic)

            self.fade.start()
            self.shrink.start()
            self.fade.finished.connect(self.final_minimize)
        elif action == "close":
            self.fade.start()
            self.fade.finished.connect(self.final_close)

    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            if hasattr(self, "original_geometry"):
                self.tray_restore()

    def tray_restore(self):
        self.setVisible(True)
        self.showNormal()
        self.raise_()
        self.activateWindow()
        self.setWindowOpacity(1)

    def animated_restore(self):
        self.setWindowOpacity(0)
        self.show()

        def start_animation():
            if not hasattr(self, "original_geometry"):
                self.original_geometry = self.geometry()

            start_rect = QRectF(self.original_geometry.center(), QSize(10, 10)).toRect()
            self.setGeometry(start_rect)

            geo_anim = QPropertyAnimation(self, b"geometry", self)
            geo_anim.setStartValue(start_rect)
            geo_anim.setEndValue(self.original_geometry)
            geo_anim.setDuration(400)
            geo_anim.setEasingCurve(QEasingCurve.OutBack)

            opacity_anim = QPropertyAnimation(self, b"windowOpacity", self)
            opacity_anim.setStartValue(0)
            opacity_anim.setEndValue(1)
            opacity_anim.setDuration(400)
            opacity_anim.setEasingCurve(QEasingCurve.InOutQuad)

            geo_anim.start()
            opacity_anim.start()

        QTimer.singleShot(10, start_animation)

    def start_spinner(self):
        self.spinner.show()

    def stop_spinner(self, final_status):
        self.spinner.hide()
        self.status_label.setText(final_status)
    
    def final_close(self):
        self.close()

    def final_minimize(self):
        self.showMinimized()
        self.setGraphicsEffect(None)     

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
    QTimer.singleShot(0, lambda: setattr(window, 'original_geometry', window.geometry()))

    sys.exit(app.exec())
