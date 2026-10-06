from PySide6.QtGui import QAction, QFont, QIcon
from PySide6.QtWidgets import QApplication, QMenu, QSystemTrayIcon

from ui.icons import icon


def create_tray(window, icon_path):
    tray_icon = QSystemTrayIcon(QIcon(icon_path), window)
    tray_icon.setToolTip("CypherGate VPN — Disconnected")

    tray_menu = QMenu()

    status_action = QAction("●  Disconnected", window)
    status_font = QFont()
    status_font.setBold(True)
    status_action.setFont(status_font)
    status_action.setEnabled(False)
    tray_menu.addAction(status_action)

    tray_menu.addSeparator()

    connect_action = QAction(
        icon("connect", "systray"),
        "Connect",
        window,
    )
    connect_action.triggered.connect(window.connect_vpn)
    tray_menu.addAction(connect_action)

    auto_connect_action = QAction(
        icon("auto_connect"),
        "Auto-connect fastest",
        window,
    )
    auto_connect_action.triggered.connect(window.auto_connect_fastest)
    tray_menu.addAction(auto_connect_action)

    cancel_action = QAction(
        icon("cancel", "systray"),
        "Cancel connection",
        window,
    )
    cancel_action.triggered.connect(window.cancel_connection)
    tray_menu.addAction(cancel_action)

    disconnect_action = QAction(
        icon("disconnect", "systray"),
        "Disconnect",
        window,
    )
    disconnect_action.triggered.connect(window.disconnect_vpn)
    tray_menu.addAction(disconnect_action)

    tray_menu.addSeparator()

    show_action = QAction(
        icon("show", "systray"),
        "Open CypherGate",
        window,
    )
    show_action.triggered.connect(window.tray_restore)
    tray_menu.addAction(show_action)

    tray_menu.addSeparator()

    exit_action = QAction(
        icon("exit", "systray"),
        "Exit",
        window,
    )
    exit_action.triggered.connect(QApplication.quit)
    tray_menu.addAction(exit_action)

    window.tray_actions = {
        "status": status_action,
        "connect": connect_action,
        "auto_connect": auto_connect_action,
        "cancel": cancel_action,
        "disconnect": disconnect_action,
        "show": show_action,
        "exit": exit_action,
    }

    tray_icon.setContextMenu(tray_menu)
    tray_icon.activated.connect(window.on_tray_icon_activated)
    tray_icon.show()

    return tray_icon
