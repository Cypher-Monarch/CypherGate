from pathlib import Path

from config.fallback_theme import FALLBACK_THEME
from config.manager import load_settings
from constants import THEME_DIR


def resolve_theme_path() -> Path:
    settings = load_settings()

    theme = settings["theme"]

    if theme["mode"] == "custom":
        return Path(theme["path"])

    return Path(THEME_DIR) / f"{theme['name']}.qss"


def load_theme() -> str:
    theme_path = resolve_theme_path()
    print(theme_path, flush=True)

    if not theme_path.exists():
        return FALLBACK_THEME

    return theme_path.read_text(
        encoding="utf-8",
    )
