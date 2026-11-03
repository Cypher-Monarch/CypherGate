#!/usr/bin/env python3

import json

from daemon.commands import (
    disable_ipv6,
    enable_ipv6,
    get_status,
    start_vpn,
    stop_vpn,
)
from daemon.setup import create_server

server = create_server()

print("[cyphergated] Listening...", flush=True)

while True:
    conn, _ = server.accept()

    try:
        data = conn.recv(4096).decode()

        if not data.strip():
            continue

        print("[cyphergated] Received:", data, flush=True)

        cmd = json.loads(data)

        match cmd.get("action"):
            case "START_VPN":
                start_vpn(cmd)

            case "STOP_VPN":
                stop_vpn()

            case "DISABLE_IPV6":
                disable_ipv6()

            case "ENABLE_IPV6":
                enable_ipv6()

            case "STATUS":
                conn.send(get_status())

    except Exception as e:
        print("Error:", e, flush=True)

    finally:
        conn.close()
