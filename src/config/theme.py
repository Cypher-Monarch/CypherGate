from pathlib import Path

THEME_DIR = Path(__file__).parent.parent / "themes"


def load_theme(name):
    theme_path = THEME_DIR / f"{name}.qss"

    if not theme_path.exists():
        return ""

    return theme_path.read_text(encoding="utf-8")
