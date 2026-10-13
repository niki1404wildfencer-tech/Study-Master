import json
from pathlib import Path
from PySide6.QtCore import Signal, QObject
from managers.app_paths import data_file

class SettingsManager(QObject):

    settings_changed = Signal()

    _shared_instance = None

    def __new__(cls, *args, **kwargs):
        if cls._shared_instance is None:
            cls._shared_instance = super().__new__(cls)
        return cls._shared_instance

    def __init__(self):
        if getattr(self, "_initialized", False):
            return
        self._initialized = True

        super().__init__()
        self.file_path = data_file("setting.json")
        self.settings = {}
        self.load()

    # =====================================================
    # Storage
    # =====================================================

    def load(self):
        if not self.file_path.exists():
            self.settings = {"daily_goal_minutes": 240}
            self.save()
            return
        try:
            with self.file_path.open("r", encoding="utf-8") as file:
                data = json.load(file)
            if isinstance(data, dict):
                self.settings = data
            else:
                self.settings = {}
        except (json.JSONDecodeError, OSError):
            self.settings = {}

    def save(self):
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        with self.file_path.open("w", encoding="utf-8") as file:
            json.dump(self.settings, file, indent=4, ensure_ascii=False)

    # =====================================================
    # Daily goal
    # =====================================================

    def get_daily_goal_minutes(self):
        value = self.settings.get("daily_goal_minutes", 0)
        try:
            return int(value)
        except (TypeError, ValueError):
            return 0

    def set_daily_goal_minutes(self, minutes):
        try:
            minutes = int(minutes)
        except (TypeError, ValueError):
            return False
        if minutes <= 0:
            return False
        self.settings["daily_goal_minutes"] = minutes
        self.save()
        self.settings_changed.emit()
        return True


def get_settings_manager() -> SettingsManager:
    return SettingsManager()