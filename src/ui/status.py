def sync_ui_state(window, state):

    if state is None:
        return

    status = state["status"]

    if status == "DISCONNECTED":
        window.stop_spinner("Disconnected")

        window.connect_btn.setEnabled(True)
        window.disconnect_btn.setEnabled(False)
        window.refresh_btn.setEnabled(True)
        window.auto_btn.setEnabled(True)

        window.cancel_button.hide()

    elif status == "CONNECTING":
        window.start_spinner()

        window.status_label.setText("Connection in progress...")

        window.connect_btn.setEnabled(False)
        window.disconnect_btn.setEnabled(False)
        window.refresh_btn.setEnabled(False)
        window.auto_btn.setEnabled(False)

        window.cancel_button.show()
        window.cancel_button.setEnabled(True)

    elif status == "CONNECTED":
        country = state.get("country") or "VPN"

        window.stop_spinner(f"Connected to {country}")

        window.connect_btn.setEnabled(False)
        window.disconnect_btn.setEnabled(True)
        window.refresh_btn.setEnabled(False)
        window.auto_btn.setEnabled(False)

        window.cancel_button.hide()

    elif status == "ERROR":
        window.stop_spinner("Connection failed")

        window.status_label.setText(state.get("last_error") or "Connection failed")

        window.connect_btn.setEnabled(True)
        window.disconnect_btn.setEnabled(False)
        window.refresh_btn.setEnabled(True)
        window.auto_btn.setEnabled(True)

        window.cancel_button.hide()
