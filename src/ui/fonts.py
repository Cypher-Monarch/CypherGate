# ────────────────────────────────────────────────────────
# Font loader
# Author: nox-lux
# ────────────────────────────────────────────────────────

from constants import FONT_DIR
from PySide6.QtGui import QFontDatabase
from pathlib import Path

SUPPORTED_FORMATS = {".ttf", ".otf"}

def load_fonts():
    font_ids = []

    for font_path in Path(FONT_DIR).iterdir():
        if font_path.suffix.lower() not in SUPPORTED_FORMATS:
            continue

        font_id = QFontDatabase.addApplicationFont(str(font_path))

        if font_id == -1:
            print(f"Failed to load font: {font_path.name}")
            continue

        font_ids.append(font_id)

    return font_ids
