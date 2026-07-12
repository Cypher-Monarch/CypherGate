from PySide6.QtWidgets import QApplication, QMenu, QSystemTrayIcon
from PySide6.QtGui import QAction, QIcon


def create_tray(window, icon_path):
    tray_icon = QSystemTrayIcon(QIcon(icon_path), window)
    tray_icon.setToolTip("🌐 CypherGate VPN")

    tray_menu = QMenu()

    show_action = QAction("👁️ Show", window)
    show_action.triggered.connect(window.show)
    tray_menu.addAction(show_action)

    connect_action = QAction("🔗 Connect", window)
    connect_action.triggered.connect(window.connect_vpn)
    tray_menu.addAction(connect_action)

    disconnect_action = QAction("❌ Disconnect", window)
    disconnect_action.triggered.connect(window.disconnect_vpn)
    tray_menu.addAction(disconnect_action)

    exit_action = QAction("🚪 Exit", window)
    exit_action.triggered.connect(QApplication.quit)
    tray_menu.addAction(exit_action)

    tray_icon.setContextMenu(tray_menu)
    tray_icon.activated.connect(window.on_tray_icon_activated)
    tray_icon.show()

    return tray_icon
