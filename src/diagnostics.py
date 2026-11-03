import platform
import shlex

import PySide6
from PySide6.QtCore import qVersion

from constants import VERSION


def _read_distro_name():
    """Read the human-readable distribution name from os-release."""

    try:
        with open("/etc/os-release", encoding="utf-8") as file:
            for line in file:
                if line.startswith("PRETTY_NAME="):
                    value = line.partition("=")[2].strip()
                    parts = shlex.split(value, comments=False)

                    if parts:
                        return " ".join(parts)

    except (OSError, UnicodeError, ValueError):
        pass

    return platform.system() or "Unknown"


def _safe_label(value, fallback="Unknown"):
    """Keep externally supplied labels on one line."""

    if value is None:
        return fallback

    value = " ".join(str(value).split())
    return value[:120] or fallback


def collect_diagnostics(settings=None, daemon_status=None):
    """
    Collect privacy-preserving application diagnostics.

    Only explicitly approved fields are included.
    No server metadata, configuration contents, paths, or logs are collected.
    """

    settings_available = isinstance(settings, dict)
    daemon_available = isinstance(daemon_status, dict)

    theme = "Unknown"

    if settings_available:
        theme_settings = settings.get("theme", {})

        if isinstance(theme_settings, dict):
            if theme_settings.get("mode") == "custom":
                theme = "Custom"
            else:
                theme = _safe_label(theme_settings.get("name"))

    vpn_state = "Unknown"

    if daemon_available:
        vpn_state = _safe_label(
            daemon_status.get("status"),
        )

    return {
        "Application": {
            "CypherGate": VERSION,
            "Python": platform.python_version(),
            "PySide6": PySide6.__version__,
            "Qt": qVersion(),
        },
        "System": {
            "Distribution": _read_distro_name(),
            "Architecture": platform.machine() or "Unknown",
        },
        "Application Status": {
            "Configuration": ("Available" if settings_available else "Unavailable"),
            "Theme": theme,
            "Daemon": ("Available" if daemon_available else "Unavailable"),
        },
        "VPN Status": {
            "State": vpn_state,
        },
    }


def format_diagnostics(data):
    """Format collected diagnostics into readable plain text."""

    sections = []

    for section, entries in data.items():
        lines = [section.upper()]

        for key, value in entries.items():
            lines.append(f"{key}: {value}")

        sections.append("\n".join(lines))

    report = "\n\n".join(sections)

    return (
        "===== CYPHERGATE DIAGNOSTICS =====\n\n"
        f"{report}\n\n"
        "================================="
    )
