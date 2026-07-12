import socket
import os
import subprocess
import json
import time

SOCKET_PATH = "/tmp/cyphergate-root-handler.sock"

# cleanup old socket
if os.path.exists(SOCKET_PATH):
    os.remove(SOCKET_PATH)

server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
server.bind(SOCKET_PATH)
server.listen(5)

os.chmod(SOCKET_PATH, 0o666)

print("[root-handler] Listening...", flush=True)

vpn_process = None
vpn_log_handle = None

while True:
    conn, _ = server.accept()
    try:
        data = conn.recv(4096).decode()

        if not data.strip():
            continue

        print("[root-handler] Received:", data, flush=True)

        cmd = json.loads(data)

        if cmd["action"] == "START_VPN":
            config = cmd["config"]
            log_file = cmd.get("log_file", f"/tmp/cyphergate_{int(time.time())}.log")

            print("[root-handler] START_VPN", flush=True)
            print("[root-handler] Config:", config, flush=True)
            print("[root-handler] Log file:", log_file, flush=True)

            # open log file (line buffered)
            vpn_log_handle = open(log_file, "a", buffering=1)

            vpn_process = subprocess.Popen(
                ["/usr/bin/openvpn", "--config", config],
                stdout=vpn_log_handle,
                stderr=subprocess.STDOUT,
            )

        elif cmd["action"] == "STOP_VPN":
            print("[root-handler] STOP_VPN", flush=True)

            if vpn_process:
                vpn_process.terminate()
                vpn_process.wait()
                vpn_process = None

            if vpn_log_handle:
                vpn_log_handle.close()
                vpn_log_handle = None

        elif cmd["action"] == "DISABLE_IPV6":
            print("[root-handler] DISABLE_IPV6", flush=True)
            subprocess.run(
                ["sysctl", "-w", "net.ipv6.conf.all.disable_ipv6=1"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

        elif cmd["action"] == "ENABLE_IPV6":
            print("[root-handler] ENABLE_IPV6", flush=True)
            subprocess.run(
                ["sysctl", "-w", "net.ipv6.conf.all.disable_ipv6=0"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

    except Exception as e:
        print("Error:", e, flush=True)

    finally:
        conn.close()
