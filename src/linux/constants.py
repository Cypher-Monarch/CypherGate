import os
import sys

API_URL = "http://www.vpngate.net/api/iphone/"

VPN_ROOT = os.path.expanduser("~/.config/cyphergate")
VPN_DIR = os.path.expanduser(f"{VPN_ROOT}/servers")
LOGS_DIR = os.path.join(VPN_ROOT, "logs")
CACHE_FILE = os.path.join(f"{VPN_ROOT}/cache", "serverlist.csv")
COUNTRIES_CONF = os.path.join(VPN_ROOT, "countries.conf")

SOCKET_PATH = "/tmp/cyphergate-root-handler.sock"

os.makedirs(VPN_DIR, exist_ok=True)
os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
os.makedirs(os.path.dirname(COUNTRIES_CONF), exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

if not os.path.exists(COUNTRIES_CONF):
    with open(COUNTRIES_CONF, "w") as f:
        f.write(
            "# Example:\nJapan\nUnited States\nIndia\nGermany\nBrazil\nViet Nam\n Korea Republic of\nRussian Federation\nThailand\nChina"
        )

if getattr(sys, "frozen", False):
    APP_DIR = os.path.dirname(sys.executable)
    ROOT_HANDLER_PATH = os.path.join(APP_DIR, "cyphergated")
else:
    APP_DIR = os.path.dirname(os.path.abspath(__file__))
    ROOT_HANDLER_PATH = os.path.join(APP_DIR, "cyphergated.py")


ICON_PATH = os.path.join(APP_DIR, "Assets", "icon.png")

VERSION = "2.0.0"
