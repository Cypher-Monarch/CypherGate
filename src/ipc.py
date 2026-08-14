import json
import os
import socket
import subprocess
import time

from constants import ROOT_HANDLER_PATH, SOCKET_PATH


def ensure_root_handler():
    if not os.path.exists(SOCKET_PATH):
        subprocess.Popen(
            ["pkexec", ROOT_HANDLER_PATH],
            start_new_session=True,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        print("Using ROOT_HANDLER_PATH at:", ROOT_HANDLER_PATH)

    for _ in range(10):
        if os.path.exists(SOCKET_PATH):
            try:
                with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
                    sock.connect(SOCKET_PATH)
                return
            except OSError:
                time.sleep(0.2)


def send_root_command(cmd_dict):
    for _ in range(5):
        try:
            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
                sock.settimeout(1)
                sock.connect(SOCKET_PATH)

                sock.sendall(json.dumps(cmd_dict).encode())

                try:
                    response = sock.recv(4096)
                except TimeoutError:
                    return None

                if response:
                    return json.loads(response.decode())

                return None

        except Exception:
            time.sleep(0.2)

    print("Root handler error: could not connect", flush=True)
    return None


def get_status():
    return send_root_command({"action": "STATUS"})
