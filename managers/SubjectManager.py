import json
from pathlib import Path
from managers.app_paths import data_file
from PySide6.QtCore import Signal, QObject


class SubjectManager(QObject):

    subject_changed = Signal()

    _shared_instance = None

    # ── Singleton ──
    def __new__(cls, *args, **kwargs):
        if cls._shared_instance is None:
            cls._shared_instance = super().__new__(cls)
        return cls._shared_instance

    def __init__(self):
        if getattr(self, "_initialized", False):
            return
        self._initialized = True

        super().__init__()
        self.file_path = data_file("subjects.json")
        self.subjects = []
        self.load()

    def load(self):
        if not self.file_path.exists():
            self.subjects = []
            self.save()
            return
        try:
            with self.file_path.open("r", encoding="utf-8") as file:
                data = json.load(file)
            if isinstance(data, list):
                self.subjects = data
            else:
                self.subjects = []
        except (json.JSONDecodeError, OSError):
            self.subjects = []

    def save(self):
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        with self.file_path.open("w", encoding="utf-8") as file:
            json.dump(self.subjects, file, indent=4, ensure_ascii=False)

    def _generate_id(self):
        if not self.subjects:
            return 1
        return max(
            int(subject.get("id", 0))
            for subject in self.subjects
        ) + 1

    def add_subject(self, name, color="#36ccd1"):
        name = name.strip()
        if not name:
            return None
        subject = {
            "id": self._generate_id(),
            "name": name,
            "color": color,
        }
        self.subjects.append(subject)
        self.save()
        self.subject_changed.emit()
        return subject

    def remove_subject(self, subject_id):
        original_count = len(self.subjects)
        self.subjects = [
            subject for subject in self.subjects
            if subject["id"] != subject_id
        ]
        if len(self.subjects) == original_count:
            return False

        self.save()

        try:
            from managers.CalendarManager import get_calendar_manager
            get_calendar_manager().delete_events_for_subject(subject_id)
        except Exception as e:
            print(f"[SubjectManager] cascade events failed: {e}")

        try:
            from managers.TaskManager import TaskManager
            TaskManager().remove_tasks_for_subject(subject_id)
        except Exception as e:
            print(f"[SubjectManager] cascade tasks failed: {e}")

        self.subject_changed.emit()
        return True

    def rename_subject(self, subject_id, new_name):
        for subject in self.subjects:
            if subject["id"] == subject_id:
                subject["name"] = new_name
                break
        self.save()
        self.subject_changed.emit()

    def get_subjects(self):
        return self.subjects.copy()

    def get_subject(self, subject_id):
        for subject in self.subjects:
            if subject.get("id") == subject_id:
                return subject.copy()
        return None

    def update_subject(self, subject_id, name, color):
        name = name.strip()
        if not name:
            return None
        for subject in self.subjects:
            if subject.get("id") != subject_id:
                continue
            subject["name"] = name
            subject["color"] = color
            self.save()
            self.subject_changed.emit()
            return subject.copy()
        return None