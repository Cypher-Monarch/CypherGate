import json
import os
import subprocess
import threading
import time

from constants import DAEMON_CONFIG
from daemon.logging import create_log
from daemon.monitor import monitor_connection
from daemon.state import reset_connection_state, state
from daemon.validator import validate_config


def start_vpn(cmd):
    config_path = cmd["config"]

    with open(config_path, encoding="utf-8") as f:
        config = f.read()

    validate_config(config)

    with open(DAEMON_CONFIG, "w", encoding="utf-8") as f:
        f.write(config)

    os.chmod(DAEMON_CONFIG, 0o640)

    log_file = create_log()

    print("[cyphergated] START_VPN", flush=True)

    state["status"] = "CONNECTING"
    state["config"] = DAEMON_CONFIG
    state["log_file"] = log_file
    state["started_at"] = time.time()
    state["last_error"] = None
    state["country"] = cmd.get("country")
    state["ping"] = cmd.get("ping")
    state["speed"] = cmd.get("speed")
    state["users"] = cmd.get("users")
    state["country_short"] = cmd.get("country_short")
    state["hostname"] = cmd.get("hostname")
    state["ip"] = cmd.get("ip")
    state["score"] = cmd.get("score")

    state["log_handle"] = open(log_file, "a", buffering=1)

    try:
        state["process"] = subprocess.Popen(
            ["/usr/bin/openvpn", "--config", DAEMON_CONFIG],
            stdout=state["log_handle"],
            stderr=subprocess.STDOUT,
        )

        state["monitor_stop"].clear()

        state["monitor_thread"] = threading.Thread(
            target=monitor_connection,
            daemon=True,
        )

        state["monitor_thread"].start()

    except Exception:
        if state["log_handle"]:
            state["log_handle"].close()
            state["log_handle"] = None

        state["status"] = "ERROR"
        raise


def stop_vpn():
    print("[cyphergated] STOP_VPN", flush=True)

    if state["process"]:
        state["process"].terminate()
        state["process"].wait()
        state["process"] = None

    try:
        os.unlink(DAEMON_CONFIG)
    except FileNotFoundError:
        pass

    if state["log_handle"]:
        state["log_handle"].close()
        state["log_handle"] = None

    state["monitor_stop"].set()

    if state["monitor_thread"] is not None:
        state["monitor_thread"].join(timeout=1)
        state["monitor_thread"] = None

    reset_connection_state()


def disable_ipv6():
    print("[cyphergated] DISABLE_IPV6", flush=True)

    subprocess.run(
        ["sysctl", "-w", "net.ipv6.conf.all.disable_ipv6=1"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    state["ipv6_disabled"] = True


def enable_ipv6():
    print("[cyphergated] ENABLE_IPV6", flush=True)

    subprocess.run(
        ["sysctl", "-w", "net.ipv6.conf.all.disable_ipv6=0"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    state["ipv6_disabled"] = False


def get_status():
    return json.dumps(
        {
            "status": state["status"],
            "country": state["country"],
            "country_short": state["country_short"],
            "hostname": state["hostname"],
            "ip": state["ip"],
            "score": state["score"],
            "ping": state["ping"],
            "speed": state["speed"],
            "users": state["users"],
            "config": state["config"],
            "log_file": state["log_file"],
            "started_at": state["started_at"],
            "ipv6_disabled": state["ipv6_disabled"],
            "last_error": state["last_error"],
        }
    ).encode()
