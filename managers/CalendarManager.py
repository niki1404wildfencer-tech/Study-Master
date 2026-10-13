import json
from datetime import datetime
from PySide6.QtCore import Signal, QObject
from managers.app_paths import data_file


class CalendarManager(QObject):

    event_changed = Signal()

    def __init__(self):
        super().__init__()
        self.file_path = data_file("events.json")
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        self.events = []
        self.load()

    # ═══════════════════════════════════════════
    # Storage
    # ═══════════════════════════════════════════
    def load(self):
        if not self.file_path.exists():
            self.events = []
            self.save()
            return
        try:
            with self.file_path.open("r", encoding="utf-8") as file:
                data = json.load(file)
            self.events = data if isinstance(data, list) else []
        except (json.JSONDecodeError, OSError):
            self.events = []

    def save(self):
        with self.file_path.open("w", encoding="utf-8") as file:
            json.dump(self.events, file, indent=4, ensure_ascii=False)

    # ═══════════════════════════════════════════
    # ID
    # ═══════════════════════════════════════════
    def _generate_id(self):
        if not self.events:
            return 1
        return max(int(e.get("id", 0)) for e in self.events) + 1

    # ═══════════════════════════════════════════
    # Create
    # ═══════════════════════════════════════════
    def add_event(
        self,
        title,
        date,
        time="09:00",
        color="#4F7CFF",
        details="",
        subject_id=None,
        task_id=None,
        repeat="none",
        reminders=None,
    ):
        event = {
            "id": self._generate_id(),
            "title": title.strip(),
            "date": date,
            "time": time,
            "color": color,
            "details": details.strip(),
            "subject_id": subject_id,
            "task_id": task_id,
            "repeat": repeat or "none",
            "reminders": reminders or [],
            "created_at": datetime.now().isoformat(timespec="seconds"),
        }
        self.events.append(event)
        self.save()
        self.event_changed.emit()
        return event

    # ═══════════════════════════════════════════
    # Read
    # ═══════════════════════════════════════════
    def get_events(self):
        return self.events.copy()

    def get_event(self, event_id):
        for e in self.events:
            if e.get("id") == event_id:
                return e.copy()
        return None

    def get_events_for_date(self, date_str):
        if not date_str:
            return []
        try:
            target = datetime.strptime(date_str, "%Y-%m-%d").date()
        except (ValueError, TypeError):
            return []
        results = []
        for event in self.events:
            if self._event_matches_date(event, target):
                results.append(event.copy())
        return results

    def _event_matches_date(self, event, target_date):
        try:
            event_date = datetime.strptime(
                event.get("date", ""), "%Y-%m-%d"
            ).date()
        except (ValueError, TypeError):
            return False

        repeat = event.get("repeat", "none")
        if repeat == "none":
            return event_date == target_date
        if target_date < event_date:
            return False

        delta_days = (target_date - event_date).days
        if repeat == "daily":
            return True
        if repeat == "weekly":
            return delta_days % 7 == 0
        if repeat == "monthly":
            return target_date.day == event_date.day
        if repeat == "yearly":
            return (
                target_date.day == event_date.day
                and target_date.month == event_date.month
            )
        return event_date == target_date

    def get_all_events_sorted(self, ascending=True):
        evs = self.events.copy()
        evs.sort(
            key=lambda e: (e.get("date", ""), e.get("time", "00:00")),
            reverse=not ascending,
        )
        return evs

    def get_upcoming_events(self, days=7):
        from datetime import timedelta
        today = datetime.now().date()
        end = today + timedelta(days=days)
        out = []
        for e in self.events:
            try:
                d = datetime.strptime(e.get("date", ""), "%Y-%m-%d").date()
            except Exception:
                continue
            if today <= d <= end:
                out.append(e.copy())
        out.sort(key=lambda x: (x.get("date", ""), x.get("time", "")))
        return out

    # ═══════════════════════════════════════════
    # Update
    # ═══════════════════════════════════════════
    def update_event(self, event_id, **fields):
        for event in self.events:
            if event.get("id") != event_id:
                continue
            for key, value in fields.items():
                if key in event:
                    event[key] = value
            self.save()
            self.event_changed.emit()
            return event.copy()
        return None

    # ═══════════════════════════════════════════
    # Delete
    # ═══════════════════════════════════════════
    def delete_event(self, event_id):
        original = len(self.events)
        self.events = [e for e in self.events if e.get("id") != event_id]
        if len(self.events) == original:
            return False
        self.save()
        self.event_changed.emit()
        return True

    def delete_events_for_subject(self, subject_id):
        original = len(self.events)
        self.events = [
            e for e in self.events if e.get("subject_id") != subject_id
        ]
        removed = original - len(self.events)
        if removed:
            self.save()
            self.event_changed.emit()
        return removed

    def delete_events_for_task(self, task_id):
        original = len(self.events)
        self.events = [
            e for e in self.events if e.get("task_id") != task_id
        ]
        removed = original - len(self.events)
        if removed:
            self.save()
            self.event_changed.emit()
        return removed


# =====================================================
# SINGLETON
# =====================================================

_shared_instance = None


def get_calendar_manager() -> CalendarManager:
    global _shared_instance
    if _shared_instance is None:
        _shared_instance = CalendarManager()
    return _shared_instance