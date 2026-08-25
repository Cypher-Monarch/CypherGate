from pathlib import Path

from PySide6.QtCore import QFileSystemWatcher, QObject, QTimer, Signal

from config.theme import resolve_theme_path


class ConfigWatcher(QObject):
    changed = Signal(str)

    def __init__(self, settings_path: Path, parent=None):
        super().__init__(parent)

        self.settings_path = settings_path
        self.theme_path: Path | None = None

        self.pending_path: str | None = None

        self.watcher = QFileSystemWatcher(self)

        self.reload_timer = QTimer(self)
        self.reload_timer.setSingleShot(True)
        self.reload_timer.setInterval(200)
        self.reload_timer.timeout.connect(self._emit_changed)

        self.watcher.fileChanged.connect(self._file_changed)

        self.watch(settings_path)
        self.refresh_theme()

    def watch(self, path: Path):
        if not path.exists():
            return

        path_str = str(path)

        if path_str not in self.watcher.files():
            self.watcher.addPath(path_str)

    def unwatch(self, path: Path):
        path_str = str(path)

        if path_str in self.watcher.files():
            self.watcher.removePath(path_str)

    def refresh_theme(self):
        new_theme = resolve_theme_path()

        if self.theme_path == new_theme:
            return

        if self.theme_path is not None:
            self.unwatch(self.theme_path)

        self.theme_path = new_theme

        self.watch(new_theme)

    def _file_changed(self, path: str):
        self.pending_path = path
        self.reload_timer.start()

    def _emit_changed(self):
        if self.pending_path is None:
            return

        path = self.pending_path
        self.pending_path = None

        changed_path = Path(path)

        self.changed.emit(path)

        # Editors like VS Code may replace files instead of modifying them.
        # Re-add the path if Qt lost track of it.
        if not changed_path.exists():
            return

        if path not in self.watcher.files():
            self.watcher.addPath(path)
