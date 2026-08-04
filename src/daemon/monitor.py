from daemon.state import state


def monitor_connection():
    while not state["monitor_stop"].is_set():
        try:
            if state["process"] and state["process"].poll() is not None:
                if state["status"] == "CONNECTING":
                    state["status"] = "ERROR"
                    state["last_error"] = "OpenVPN exited unexpectedly"
                break

            if state["log_file"]:
                with open(state["log_file"], encoding="utf-8") as log:
                    if "Initialization Sequence Completed" in log.read():
                        state["status"] = "CONNECTED"
                        break

        except OSError:
            pass

        state["monitor_stop"].wait(0.5)
