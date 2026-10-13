import json
from managers.app_paths import data_file
from PySide6.QtCore import Signal, QObject


_UNSET = object()


class TaskManager(QObject):

    task_changed = Signal()

    _shared_instance = None

    VALID_PRIORITIES = ("critical", "high", "medium", "low")
    DEFAULT_PRIORITY = "medium"

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
        self.file_path = data_file("tasks.json")
        self.tasks = []
        self.load()

    # =====================================================
    # STORAGE
    # =====================================================

    def load(self):
        if not self.file_path.exists():
            self.tasks = []
            self.save()
            return
        try:
            with self.file_path.open("r", encoding="utf-8") as file:
                data = json.load(file)
            if isinstance(data, list):
                self.tasks = data
            else:
                self.tasks = []
        except (json.JSONDecodeError, OSError):
            self.tasks = []
        self._cleanup_orphans()
        self._backfill_priorities()

    def _cleanup_orphans(self):
        from managers.SubjectManager import SubjectManager
        subjects = SubjectManager().get_subjects()
        if not subjects:
            return
        valid_ids = {s["id"] for s in subjects}
        original = len(self.tasks)
        self.tasks = [
            t for t in self.tasks
            if t.get("subject_id") is None
            or t.get("subject_id") in valid_ids
        ]
        if len(self.tasks) != original:
            self.save()

    def _backfill_priorities(self):
        changed = False
        for task in self.tasks:
            if "priority" not in task:
                task["priority"] = self.DEFAULT_PRIORITY
                changed = True
        if changed:
            self.save()

    def save(self):
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        with self.file_path.open("w", encoding="utf-8") as file:
            json.dump(self.tasks, file, indent=4, ensure_ascii=False)

    def _generate_id(self):
        if not self.tasks:
            return 1
        return max(int(task.get("id", 0)) for task in self.tasks) + 1

    # =====================================================
    # CREATE
    # =====================================================

    def add_task(self, subject_id, name, priority=None):
        name = name.strip()
        if not name:
            return None
        if priority not in self.VALID_PRIORITIES:
            priority = self.DEFAULT_PRIORITY
        task = {
            "id": self._generate_id(),
            "subject_id": subject_id,
            "name": name,
            "completed": False,
            "priority": priority,
        }
        self.tasks.append(task)
        self.save()
        self.task_changed.emit()
        return task

    # =====================================================
    # READ
    # =====================================================

    def get_tasks(self, subject_id):
        return [
            task.copy()
            for task in self.tasks
            if task.get("subject_id") == subject_id
        ]

    def get_task(self, task_id):
        for task in self.tasks:
            if task.get("id") == task_id:
                return task.copy()
        return None

    def get_all_tasks(self):
        return [t.copy() for t in self.tasks]

    def get_tasks_by_priority(self, priority=None):
        order = {p: i for i, p in enumerate(self.VALID_PRIORITIES)}

        def sort_key(t):
            return (
                bool(t.get("completed", False)),
                order.get(t.get("priority", self.DEFAULT_PRIORITY), 99),
                t.get("id", 0),
            )

        result = [
            t.copy()
            for t in self.tasks
            if priority is None or t.get("priority") == priority
        ]
        result.sort(key=sort_key)
        return result

    def count_by_priority(self, priority=None):
        if priority is None:
            return len(self.tasks)
        return sum(1 for t in self.tasks if t.get("priority") == priority)

    # =====================================================
    # UPDATE
    # =====================================================

    def update_task(self, task_id, name, priority=_UNSET, subject_id=_UNSET):
        name = name.strip()
        if not name:
            return None
        for task in self.tasks:
            if task.get("id") != task_id:
                continue
            task["name"] = name
            if priority is not _UNSET and priority in self.VALID_PRIORITIES:
                task["priority"] = priority
            if subject_id is not _UNSET:
                task["subject_id"] = subject_id
            self.save()
            self.task_changed.emit()
            return task.copy()
        return None

    def set_completed(self, task_id, completed):
        for task in self.tasks:
            if task.get("id") != task_id:
                continue
            task["completed"] = bool(completed)
            self.save()
            self.task_changed.emit()
            return True
        return False

    def set_priority(self, task_id, priority):
        if priority not in self.VALID_PRIORITIES:
            return False
        for task in self.tasks:
            if task.get("id") != task_id:
                continue
            task["priority"] = priority
            self.save()
            self.task_changed.emit()
            return True
        return False

    # =====================================================
    # DELETE
    # =====================================================

    def remove_task(self, task_id):
        original_count = len(self.tasks)
        self.tasks = [
            task for task in self.tasks
            if task.get("id") != task_id
        ]
        if len(self.tasks) == original_count:
            return False
        self.save()
        self.task_changed.emit()
        return True

    def remove_tasks_for_subject(self, subject_id):
        original = len(self.tasks)
        self.tasks = [
            t for t in self.tasks if t.get("subject_id") != subject_id
        ]
        removed = original - len(self.tasks)
        if removed:
            self.save()
            self.task_changed.emit()
        return removed