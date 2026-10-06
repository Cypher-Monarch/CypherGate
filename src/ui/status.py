def sync_ui_state(window, state):
    if state is None:
        return

    status = state["status"]
    actions = window.tray_actions

    if status == "DISCONNECTED":
        window.stop_spinner("Disconnected")

        window.connect_btn.setEnabled(True)
        window.disconnect_btn.setEnabled(False)
        window.refresh_btn.setEnabled(True)
        window.auto_btn.setEnabled(True)
        window.cancel_button.hide()

        actions["status"].setText("● Disconnected")
        actions["connect"].setVisible(True)
        actions["auto_connect"].setVisible(True)
        actions["cancel"].setVisible(False)
        actions["disconnect"].setVisible(False)
        window.tray_icon.setToolTip("CypherGate VPN — Disconnected")

    elif status == "CONNECTING":
        window.start_spinner()
        window.status_label.setText("Connection in progress...")

        window.connect_btn.setEnabled(False)
        window.disconnect_btn.setEnabled(False)
        window.refresh_btn.setEnabled(False)
        window.auto_btn.setEnabled(False)
        window.cancel_button.show()
        window.cancel_button.setEnabled(True)

        actions["status"].setText("◌ Connecting…")
        actions["connect"].setVisible(False)
        actions["auto_connect"].setVisible(False)
        actions["cancel"].setVisible(True)
        actions["disconnect"].setVisible(False)
        window.tray_icon.setToolTip("CypherGate VPN — Connecting…")

    elif status == "CONNECTED":
        country = state.get("country") or "VPN"
        ping = state.get("ping")

        window.stop_spinner(f"Connected to {country}")

        window.connect_btn.setEnabled(False)
        window.disconnect_btn.setEnabled(True)
        window.refresh_btn.setEnabled(False)
        window.auto_btn.setEnabled(False)
        window.cancel_button.hide()

        status_text = f"Connected to {country}"
        if ping is not None:
            status_text += f" — {ping}"

        actions["status"].setText(f"● {status_text}")
        actions["connect"].setVisible(False)
        actions["auto_connect"].setVisible(False)
        actions["cancel"].setVisible(False)
        actions["disconnect"].setVisible(True)
        window.tray_icon.setToolTip(f"CypherGate VPN — {status_text}")

    elif status == "ERROR":
        error = state.get("last_error") or "Connection failed"

        window.stop_spinner("Connection failed")
        window.status_label.setText(error)

        window.connect_btn.setEnabled(True)
        window.disconnect_btn.setEnabled(False)
        window.refresh_btn.setEnabled(True)
        window.auto_btn.setEnabled(True)
        window.cancel_button.hide()

        actions["status"].setText("! Connection failed")
        actions["connect"].setVisible(True)
        actions["auto_connect"].setVisible(True)
        actions["cancel"].setVisible(False)
        actions["disconnect"].setVisible(False)
        window.tray_icon.setToolTip(f"CypherGate VPN — {error}")
