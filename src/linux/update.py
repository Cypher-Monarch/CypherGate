import requests
from PySide6.QtWidgets import QMessageBox

from constants import VERSION

# ────────────────────────────────────────────────────────
# Update Check
# ────────────────────────────────────────────────────────


def check_for_updates(self):
    try:
        response = requests.get(
            "https://raw.githubusercontent.com/Cypher-Monarch/CypherGate/main/Versions/linux_version.txt",
            timeout=5,
        )
        latest_version = response.text.strip()
        if latest_version != VERSION:
            QMessageBox.information(
                self,
                "Update Available",
                f"A new version {latest_version} is available! Please update for the latest features and fixes.",
            )
    except requests.RequestException as e:
        QMessageBox.warning(
            self,
            "Update Check Failed",
            f"Could not check for updates: {e}\nYou can manually check on GitHub.",
        )
