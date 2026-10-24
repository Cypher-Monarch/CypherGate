def sync_ui_state(window, state):
    if state is None:
        return

    status = state["status"]
    actions = window.tray_actions

    server_fetch_error = getattr(window, "server_fetch_error", False)

    if status == "DISCONNECTED":
        if not server_fetch_error:
            window.stop_spinner("Disconnected")
        else:
            window.spinner.hide()

        window.connect_btn.setEnabled(not server_fetch_error)
        window.disconnect_btn.setEnabled(False)
        window.refresh_btn.setEnabled(True)
        window.auto_btn.setEnabled(not server_fetch_error)
        window.cancel_button.hide()

        if not server_fetch_error:
            actions["status"].setText("● Disconnected")
            window.tray_icon.setToolTip("CypherGate VPN — Disconnected")

        actions["connect"].setVisible(not server_fetch_error)
        actions["auto_connect"].setVisible(not server_fetch_error)
        actions["cancel"].setVisible(False)
        actions["disconnect"].setVisible(False)

    elif status == "CONNECTING":
        if not server_fetch_error:
            window.start_spinner()
            window.status_label.setText("Connection in progress...")
        else:
            window.spinner.hide()

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

        if not server_fetch_error:
            window.stop_spinner(f"Connected to {country}")
        else:
            window.spinner.hide()

        window.connect_btn.setEnabled(False)
        window.disconnect_btn.setEnabled(True)
        window.refresh_btn.setEnabled(False)
        window.auto_btn.setEnabled(False)
        window.cancel_button.hide()

        status_text = f"Connected to {country}"
        if ping is not None:
            status_text += f" — {ping}"

        if not server_fetch_error:
            window.status_label.setText(status_text)

        actions["status"].setText(f"● {status_text}")
        actions["connect"].setVisible(False)
        actions["auto_connect"].setVisible(False)
        actions["cancel"].setVisible(False)
        actions["disconnect"].setVisible(True)
        window.tray_icon.setToolTip(f"CypherGate VPN — {status_text}")

    elif status == "ERROR":
        error = state.get("last_error") or "Connection failed"

        if not server_fetch_error:
            window.stop_spinner("Connection failed")
            window.status_label.setText(error)
        else:
            window.spinner.hide()

        window.connect_btn.setEnabled(not server_fetch_error)
        window.disconnect_btn.setEnabled(False)
        window.refresh_btn.setEnabled(True)
        window.auto_btn.setEnabled(not server_fetch_error)
        window.cancel_button.hide()

        actions["status"].setText("! Connection failed")
        actions["connect"].setVisible(not server_fetch_error)
        actions["auto_connect"].setVisible(not server_fetch_error)
        actions["cancel"].setVisible(False)
        actions["disconnect"].setVisible(False)
        window.tray_icon.setToolTip(f"CypherGate VPN — {error}")
