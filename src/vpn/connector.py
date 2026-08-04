import base64
import os
import re
import subprocess

from constants import VPN_DIR


def extract_remote_host(config):
    match = re.search(r"^remote\s+([^\s]+)", config, re.MULTILINE)
    return match.group(1) if match else None


def server_supports_ipv6(host):
    try:
        result = False
        result = subprocess.run(
            ["dig", "AAAA", host, "+short"],
            capture_output=True,
            text=True,
            timeout=2,
        )
        return bool(result.stdout.strip())
    except Exception:
        return False


def prepare_connection(server):
    country, _, _, _, config_b64 = server

    ovpn_path = os.path.join(VPN_DIR, f"{country}.ovpn")

    config = base64.b64decode(config_b64).decode(errors="ignore")

    if "data-ciphers" not in config:
        config += (
            "\ndata-ciphers AES-256-GCM:AES-128-GCM:CHACHA20-POLY1305:AES-128-CBC\n"
        )

    if "cipher" not in config:
        config += "\ncipher AES-128-CBC\n"

    disable_ipv6 = False

    host = extract_remote_host(config)

    if host and server_supports_ipv6(host):
        if "tun-ipv6" not in config:
            config += (
                "\n".join(
                    [
                        "",
                        "tun-ipv6",
                        "push-peer-info",
                        "redirect-gateway def1 ipv6",
                        "route-ipv6 2000::/3 ::1",
                    ]
                )
                + "\n"
            )
    else:
        disable_ipv6 = True

    return config, ovpn_path, disable_ipv6


def write_config(config, path):
    with open(path, "w") as f:
        f.write(config)
