import threading

state = {
    "status": "DISCONNECTED",
    "process": None,
    "log_handle": None,
    "country": None,
    "config": None,
    "log_file": None,
    "started_at": None,
    "ipv6_disabled": False,
    "last_error": None,
    "monitor_thread": None,
    "monitor_stop": threading.Event(),
    "users": None,
    "speed": None,
    "ping": None,
}


def reset_connection_state():
    state["status"] = "DISCONNECTED"
    state["process"] = None
    state["config"] = None
    state["log_file"] = None
    state["log_handle"] = None
    state["started_at"] = None
    state["country"] = None
    state["ping"] = None
    state["speed"] = None
    state["users"] = None
    state["last_error"] = None
