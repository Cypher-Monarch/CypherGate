import json
import os
from copy import deepcopy

from config.defaults import DEFAULT_SETTINGS
from constants import CONFIG_FILE, VPN_ROOT

_LAST_SETTINGS = None


def ensure_config():
    os.makedirs(VPN_ROOT, exist_ok=True)

    if not os.path.exists(CONFIG_FILE):
        save_settings(DEFAULT_SETTINGS)


def load_settings():
    global _LAST_SETTINGS

    ensure_config()

    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as file:
            settings = json.load(file)

    except (json.JSONDecodeError, OSError):
        if _LAST_SETTINGS is not None:
            return deepcopy(_LAST_SETTINGS)

        return deepcopy(DEFAULT_SETTINGS)

    merged = merge_defaults(settings, DEFAULT_SETTINGS)

    if merged != settings:
        save_settings(merged)

    _LAST_SETTINGS = merged

    return merged


def save_settings(settings):
    os.makedirs(VPN_ROOT, exist_ok=True)

    with open(CONFIG_FILE, "w", encoding="utf-8") as file:
        json.dump(
            settings,
            file,
            indent=4,
        )


def merge_defaults(settings, defaults):
    result = deepcopy(settings)

    for key, value in defaults.items():
        if key not in result:
            result[key] = deepcopy(value)

        elif isinstance(value, dict) and isinstance(result[key], dict):
            result[key] = merge_defaults(
                result[key],
                value,
            )

        elif not valid_type(result[key], value):
            result[key] = deepcopy(value)

    return result


def valid_type(value, expected):
    if expected is None:
        return True

    if isinstance(expected, bool):
        return isinstance(value, bool)

    return isinstance(value, type(expected))
