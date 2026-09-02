# ────────────────────────────────────────────────────────
# Font loader
# Author: nox-lux & Cypher-Monarch
# ────────────────────────────────────────────────────────

from constants import FONT_DIR, USER_FONT_DIR
from PySide6.QtGui import QFontDatabase
from pathlib import Path

SUPPORTED_FORMATS = {".ttf", ".otf"}

def load_fonts():
    font_ids = []
    font_dirs = [Path(FONT_DIR)]
    user_font_dir = Path(USER_FONT_DIR)
    if user_font_dir.is_dir():
        font_dirs.append(Path(USER_FONT_DIR))

    for font_dir in font_dirs:
        for font_path in font_dir.iterdir():
            if font_path.suffix.lower() not in SUPPORTED_FORMATS:
                continue

            font_id = QFontDatabase.addApplicationFont(str(font_path))

            if font_id == -1:
                print(f"Failed to load font: {font_path.name}")
                continue

            font_ids.append(font_id)

    return font_ids
