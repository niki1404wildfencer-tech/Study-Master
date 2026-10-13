from datetime import datetime, timedelta

from PySide6.QtCore import QObject, QTimer, Signal

from managers.CalendarManager import get_calendar_manager
from assets.SoundSystem import SoundManager


class ReminderService(QObject):

    reminder_fired = Signal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.calendar_manager = get_calendar_manager()
        self._fired_keys = set()
        self._last_check = None

        self.timer = QTimer(self)
        self.timer.setInterval(30 * 1000)
        self.timer.timeout.connect(self._tick)

    def start(self):
        self.timer.start()
        self._tick()

    def stop(self):
        self.timer.stop()

    def _resolve_reminder_datetime(self, event, reminder):
        try:
            base_date = datetime.strptime(event.get("date", ""), "%Y-%m-%d").date()
        except Exception:
            return None

        when = reminder.get("when")
        custom_date = reminder.get("custom_date")

        if when == "custom" and custom_date:
            try:
                target_date = datetime.strptime(custom_date, "%Y-%m-%d").date()
            except Exception:
                target_date = base_date
        elif when == "1_day_before":
            target_date = base_date - timedelta(days=1)
        elif when == "1_week_before":
            target_date = base_date - timedelta(days=7)
        else:
            offset = int(reminder.get("offset_days", 0) or 0)
            target_date = base_date - timedelta(days=offset)

        h = int(reminder.get("hour", 9))
        m = int(reminder.get("minute", 0))
        return datetime.combine(target_date, datetime.min.time()).replace(
            hour=h, minute=m
        )

    def _tick(self):
        now = datetime.now().replace(second=0, microsecond=0)
        if self._last_check is None:
            self._last_check = now - timedelta(minutes=1)

        for event in self.calendar_manager.get_events():
            reminders = event.get("reminders", []) or []
            for idx, reminder in enumerate(reminders):
                dt = self._resolve_reminder_datetime(event, reminder)
                if dt is None:
                    continue
                if not (self._last_check < dt <= now):
                    continue
                key = (event.get("id"), idx, dt.isoformat())
                if key in self._fired_keys:
                    continue
                self._fired_keys.add(key)
                self._fire(event, reminder)

        self._last_check = now

    def _fire(self, event, reminder):
        sound = reminder.get("sound", "None")
        if sound and sound != "None":
            SoundManager.play_completion(sound)
        self.reminder_fired.emit(event)