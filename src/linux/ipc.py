import os
import subprocess
import json
import time
import socket
from constants import ROOT_HANDLER_PATH, SOCKET_PATH

# ────────────────────────────────────────────────────────
# Helper Functions
# ────────────────────────────────────────────────────────


def ensure_root_handler():
    if not os.path.exists(SOCKET_PATH):
        subprocess.Popen(["pkexec", ROOT_HANDLER_PATH])
        print("Using ROOT_HANDLER_PATH at:", ROOT_HANDLER_PATH)

    for _ in range(10):
        if os.path.exists(SOCKET_PATH):
            try:
                sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                sock.connect(SOCKET_PATH)
                sock.close()
                return
            except Exception:
                time.sleep(0.2)


def send_root_command(cmd_dict):
    for _ in range(5):
        try:
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            sock.connect(SOCKET_PATH)
            sock.send(json.dumps(cmd_dict).encode())
            sock.close()
            return
        except Exception:
            time.sleep(0.2)

    print("Root handler error: could not connect", flush=True)
