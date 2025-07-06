import sys
import requests
import csv
import subprocess
import base64
import os
from plyer import notification
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLabel, QMessageBox, QHBoxLayout, QComboBox
)
from PySide6.QtCore import Qt

API_URL = "http://www.vpngate.net/api/iphone/"
VPN_DIR = os.path.expanduser("~/.config/cyphergate/ovpn_configs")
os.makedirs(VPN_DIR, exist_ok=True)

class CypherGate(QWidget):
    def __init__(self):
        super().__init__()
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
        """)

        layout = QVBoxLayout()

        title = QLabel("🌐 CypherGate VPN Servers")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-weight: bold; font-size: 18px;")
        layout.addWidget(title)

        # Country dropdown
        self.country_dropdown = QComboBox()
        self.country_dropdown.currentTextChanged.connect(self.filter_servers)
        layout.addWidget(self.country_dropdown)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Country", "Ping", "Speed", "Users"])
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

    def load_servers(self):
        try:
            response = requests.get(API_URL, timeout=15)
            response.raise_for_status()
            lines = response.text.splitlines()[2:]  # Skip first 2 lines
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
            self.filter_servers(self.country_dropdown.currentText())
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to fetch VPN servers:\n{e}")

    def filter_servers(self, country):
        filtered = [s for s in self.all_servers if s[0] == country]
        filtered.sort(key=lambda s: int(s[1].split()[0]))
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
                ["sudo", "openvpn", "--config", ovpn_path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CypherGate()
    window.show()
    sys.exit(app.exec())
