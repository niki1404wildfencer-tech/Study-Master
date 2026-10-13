from pathlib import Path

APP_DATA = Path.home() / ".study_master"
APP_DATA.mkdir(parents=True, exist_ok=True)


def data_file(name: str) -> Path:
    """Return an absolute path inside the user's Study Master folder."""
    return APP_DATA / name