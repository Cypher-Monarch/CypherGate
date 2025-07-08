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
    QMenu, QSizePolicy
)
from PySide6.QtGui import QIcon, QAction, QFont
from PySide6.QtCore import Qt
import time

API_URL = "http://www.vpngate.net/api/iphone/"
VPN_DIR = os.path.expanduser("~/.config/cyphergate/ovpn_configs")
CACHE_FILE = os.path.join(os.path.expanduser(f"{VPN_DIR}/cache"), "serverlist.csv")
os.makedirs(VPN_DIR, exist_ok=True)
os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)

class CypherGate(QWidget):
    def __init__(self):
        super().__init__()
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

        layout.addWidget(title_bar_widget)  # NOW it's correct 👀

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

        self.status_label = QLabel("🔓 Disconnected")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)

        self.setLayout(layout)
        self.load_servers()

        self.tray_icon = QSystemTrayIcon(QIcon("Assets/icon.png"), self)
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

    def load_servers(self):
        try:
            response = requests.get(API_URL, timeout=30)
            response.raise_for_status()
            data = response.text
            
            # Save to cache for offline use later
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
        
        # Continue parsing servers normally
        lines = data.splitlines()[2:]
        reader = csv.reader(lines)
        servers = []
        countries = set()
        for row in reader:
            if len(row) < 15:
                continue
            country = row[5]
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
        for i, (country, ping, speed, users, _) in enumerate(servers):
            self.table.setItem(i, 0, QTableWidgetItem(country))
            self.table.setItem(i, 1, QTableWidgetItem(ping))
            self.table.setItem(i, 2, QTableWidgetItem(speed))
            self.table.setItem(i, 3, QTableWidgetItem(users))
        self.table.resizeColumnsToContents()
        self.filtered_servers = servers

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
        country, ping, speed, users, config_b64 = server
        ovpn_path = os.path.join(VPN_DIR, f"{country}.ovpn")

        config = base64.b64decode(config_b64).decode(errors='ignore')
        if "data-ciphers" not in config:
            config += "\ndata-ciphers AES-256-GCM:AES-128-GCM:CHACHA20-POLY1305:AES-128-CBC\n"
        if "cipher" not in config:
            config += "\ncipher AES-128-CBC\n"

        with open(ovpn_path, "w") as f:
            f.write(config)

        try:
            self.vpn_process = subprocess.Popen(
                [r"bin\openvpn.exe", "--config", ovpn_path],
                creationflags=subprocess.CREATE_NO_WINDOW,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            time.sleep(15)
            self.status_label.setText(f"🔒 Connected to {country}")
            self.connect_btn.setEnabled(False)
            self.disconnect_btn.setEnabled(True)
            self.show_connection_info(country, ping, speed, users)
        except Exception as e:
            QMessageBox.critical(self, "Connection Failed", str(e))

    def show_connection_info(self, country, ping, speed, users):
        try:
            ip = requests.get("https://ipinfo.io/ip", timeout=10).text.strip()
        except:
            ip = "Unknown"
        msg = (f"🌐 Connected to {country}\n"
               f"🏓 Ping: {ping}\n"
               f"🚀 Speed: {speed}\n"
               f"👥 Users: {users}\n"
               f"🔑 Your new IP: {ip}")
        QMessageBox.information(self, "VPN Connected", msg)
        notification.notify(
            title="CypherGate VPN Connected",
            message=f"{country} | New IP: {ip}",
            app_name="CypherGate"
        )

    def disconnect_vpn(self):
        if self.vpn_process:
            self.vpn_process.terminate()
            self.vpn_process.wait()
            self.vpn_process = None
            self.status_label.setText("🔓 Disconnected")
            self.connect_btn.setEnabled(True)
            self.disconnect_btn.setEnabled(False)
            QMessageBox.information(self, "VPN Disconnected", "VPN connection has been terminated.")
            notification.notify(
                title="CypherGate VPN Disconnected",
                message="VPN connection has been terminated.",
                app_name="CypherGate"
            )

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("Assets/icon.png"))
    window = CypherGate()
    window.show()
    frame = window.frameGeometry()
    center_point = QApplication.primaryScreen().availableGeometry().center()
    frame.moveCenter(center_point)
    window.move(frame.topLeft())
    sys.exit(app.exec())