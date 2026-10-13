from PySide6.QtCore import (
    QTimer,
    Signal,
    QObject
)

from managers.enum.TimerState import TimerState
from managers.enum.TimerMode import TimerMode
from managers.SessionManager import get_session_manager
from assets.SoundSystem import SoundManager


class TimerManager(QObject):
    time_changed = Signal(str)
    mode_changed = Signal(TimerMode)
    state_changed = Signal(TimerState)
    finished = Signal(dict)

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
        self.timer = QTimer()
        self.timer.setInterval(1000)

        self.total_seconds = 0
        self.remaining_seconds = 0

        self.state = TimerState.STOPPED
        self.current_mode = TimerMode.FOCUS

        self.focus_duration = 25 * 60
        self.break_duration = 5 * 60
        self.long_break_duration = 15 * 60

        self.current_subject_id = None
        self.current_subject_name = "-"
        self.current_task_id = None
        self.current_task_name = "-"
        self.completion_sound = "Gentle"
        self.session_manager = get_session_manager()

        self.completed_sessions = 0
        self.daily_goal_minutes = 0
        self.today_study_minutes = 0

        self._progress_ring = None
        self._display = None
        self._controls = None
        self._session_card = None

        self.total_seconds = self.focus_duration
        self.remaining_seconds = self.focus_duration

        self.connect_signals()

    def connect_signals(self):
        self.timer.timeout.connect(self._tick)

    def set_duration_minutes(self, seconds: int):
        if seconds <= 0:
            return
        seconds *= 60
        self.focus_duration = seconds
        if self.state == TimerState.STOPPED:
            self.total_seconds = seconds
            self.remaining_seconds = seconds
            self.time_changed.emit(self.format_time())
            if self._display is not None:
                self._display.set_time(self.format_time())

    def format_time(self):
        minutes = self.remaining_seconds // 60
        seconds = self.remaining_seconds % 60
        return f"{minutes:02}:{seconds:02}"

    def _tick(self):
        self.remaining_seconds = max(0, self.remaining_seconds - 1)
        current_time = self.format_time()
        self.time_changed.emit(current_time)
        if self._display is not None:
            self._display.set_time(current_time)
        if self.remaining_seconds == 0:
            self._finished()

    def start(self):
        if self.remaining_seconds <= 0 or self.state == TimerState.RUNNING:
            return

        if self.current_mode == TimerMode.FOCUS:
            self.session_manager.start_session(
                subject_id=self.current_subject_id,
                task_id=self.current_task_id,
                planned_duration=self.total_seconds // 60
            )

        self.state = TimerState.RUNNING
        self.timer.start()
        self.state_changed.emit(self.state)

        if self._display is not None:
            if self.current_mode == TimerMode.FOCUS:
                self._display.start_focus()
            else:
                self._display.start_break()

        if self._session_card is not None:
            mode_text = "Studying..." if self.current_mode == TimerMode.FOCUS else "Break"
            self._session_card.update_session(
                self.current_subject_name,
                self.current_task_name,
                f"{self.total_seconds // 60} min",
                mode_text
            )

    def pause(self):
        if self.state != TimerState.RUNNING:
            return
        self.timer.stop()
        self.state = TimerState.PAUSED
        self.state_changed.emit(self.state)
        if self._display is not None:
            self._display.pause()

    def resume(self):
        if self.state != TimerState.PAUSED:
            return
        self.timer.start()
        self.state = TimerState.RUNNING
        self.state_changed.emit(self.state)
        if self._display is not None:
            self._display.resume()

    def restart(self):
        self.timer.stop()
        self.session_manager.cancel_session()

        if self.current_mode == TimerMode.FOCUS:
            self.total_seconds = self.focus_duration
        elif self.current_mode == TimerMode.SHORT_BREAK:
            self.total_seconds = self.break_duration
        elif self.current_mode == TimerMode.LONG_BREAK:
            self.total_seconds = self.long_break_duration

        self.remaining_seconds = self.total_seconds
        self.state = TimerState.STOPPED
        self.time_changed.emit(self.format_time())
        self.state_changed.emit(self.state)

        if self._display is not None:
            self._display.reset()
            self._display.set_time(self.format_time())
        if self._session_card is not None:
            self._session_card.clear()

    def skip(self):
        self.timer.stop()

        if self.current_mode == TimerMode.FOCUS:
            self.session_manager.cancel_session()
            self.current_mode = TimerMode.SHORT_BREAK
            self.total_seconds = self.break_duration
        elif self.current_mode == TimerMode.SHORT_BREAK:
            self.current_mode = TimerMode.FOCUS
            self.total_seconds = self.focus_duration
        else:
            self.current_mode = TimerMode.FOCUS
            self.total_seconds = self.focus_duration

        self.remaining_seconds = self.total_seconds
        self.state = TimerState.STOPPED
        self.mode_changed.emit(self.current_mode)
        self.state_changed.emit(self.state)
        self.time_changed.emit(self.format_time())

        if self._display is not None:
            self._display.reset()
            self._display.set_time(self.format_time())
        if self._controls is not None:
            self._controls.set_start()
        if self._session_card is not None:
            mode_text = "Break" if self.current_mode == TimerMode.SHORT_BREAK else "Focus"
            self._session_card.update_session(
                self.current_subject_name,
                self.current_task_name,
                f"{self.total_seconds // 60} min",
                mode_text
            )

    def _finished(self):
        self.timer.stop()
        self.state = TimerState.STOPPED

        if self.current_mode == TimerMode.FOCUS:
            self.total_seconds = self.focus_duration
        elif self.current_mode == TimerMode.SHORT_BREAK:
            self.total_seconds = self.break_duration
        else:
            self.total_seconds = self.long_break_duration

        self.remaining_seconds = self.total_seconds

        if self._controls is not None:
            self._controls.set_start()

        session = None
        try:
            if self.current_mode == TimerMode.FOCUS:
                session = self.session_manager.finish_session()
                if session is not None:
                    self.completed_sessions += 1
                    self.today_study_minutes += session["actual_duration"]
        except Exception as e:
            print(f"Error saving session: {e}")

        self.time_changed.emit(self.format_time())
        self.state_changed.emit(self.state)
        SoundManager.play_completion(self.completion_sound)

        self.finished.emit(session)

        if self._display is not None:
            self._display.finish()
        if self._session_card is not None:
            self._session_card.clear()

    def set_session_card(self, session_card):
        self._session_card = session_card

    def set_display(self, display):
        self._display = display

    def set_controls(self, controls):
        self._controls = controls

    def set_subject(self, subject_id):
        self.current_subject_id = subject_id

    def set_subject_name(self, name):
        self.current_subject_name = name if name else "-"

    def set_task(self, task_id):
        self.current_task_id = task_id

    def set_task_name(self, name):
        self.current_task_name = name if name else "-"

    def set_completion_sound(self, sound_name):
        if sound_name in SoundManager.COMPLETION_SOUNDS:
            self.completion_sound = sound_name