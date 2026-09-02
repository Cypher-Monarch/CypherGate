import os
import sys

API_URL = "http://www.vpngate.net/api/iphone/"

VPN_ROOT = os.path.expanduser("~/.config/cyphergate")
VPN_DIR = os.path.join(f"{VPN_ROOT}/servers")
CONFIG_FILE = os.path.join(VPN_ROOT, "settings.json")
LOG_DIR = "/var/log/cyphergate"
CACHE_FILE = os.path.join(f"{VPN_ROOT}/cache", "serverlist.csv")
COUNTRIES_CONF = os.path.join(VPN_ROOT, "countries.conf")

SOCKET_DIR = "/run/cyphergate"
SOCKET_PATH = f"{SOCKET_DIR}/cyphergated.sock"
DAEMON_CONFIG = f"{SOCKET_DIR}/config.ovpn"

os.makedirs(VPN_DIR, exist_ok=True)
os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
os.makedirs(os.path.dirname(COUNTRIES_CONF), exist_ok=True)

if not os.path.exists(COUNTRIES_CONF):
    with open(COUNTRIES_CONF, "w") as f:
        f.write(
            "# Example:\nJapan\nUnited States\nIndia\nGermany\nBrazil\nViet Nam\n Korea Republic of\nRussian Federation\nThailand\nChina"
        )

if getattr(sys, "frozen", False):
    APP_DIR = os.path.dirname(sys.executable)
    ROOT_HANDLER_PATH = os.path.join(APP_DIR, "cyphergated")
    THEME_DIR = "/usr/share/cyphergate/themes"
else:
    APP_DIR = os.path.dirname(os.path.abspath(__file__))
    ROOT_HANDLER_PATH = os.path.join(APP_DIR, "cyphergated.py")
    THEME_DIR = os.path.join(APP_DIR, "themes")

ICON_DIR = os.path.join(APP_DIR, "Assets", "icons")

ICON_PATH = os.path.join(APP_DIR, "Assets", "icon.png")

FONT_DIR = os.path.join(APP_DIR, "Assets", "fonts")
USER_FONT_DIR = os.path.join(VPN_ROOT,"fonts")

TABLE_COLUMNS = {
    "country": ("Country", 0),
    "ping": ("Ping", 1),
    "speed": ("Speed", 2),
    "users": ("Users", 3),
    "hostname": ("Hostname", 4),
    "ip": ("IP", 5),
    "country_short": ("Country Code", 6),
    "score": ("Score", 7),
}

VERSION = "2.0.3"
