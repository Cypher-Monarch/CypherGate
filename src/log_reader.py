from pathlib import Path


def read_log(file_path):
    """Read and return the contents of a log file."""
    try:
        return Path(file_path).read_text(
            encoding="utf-8",
            errors="replace",
        )
    except OSError as exc:
        raise OSError(f"Unable to read log file: {exc}") from exc
