import json
from managers.app_paths import data_file
from datetime import datetime

from PySide6.QtCore import Signal, QObject


class SessionManager(QObject):

    # =====================================================
    # SIGNALS
    # =====================================================

    session_started = Signal(dict)
    session_completed = Signal(dict)

    # =====================================================
    # INIT
    # =====================================================

    def __init__(self):

        super().__init__()

        self._file = data_file("sessions.json")

        self._sessions = []

        self._current_session = None

        self.load()

    # =====================================================
    # STORAGE
    # =====================================================

    def load(self):

        if not self._file.exists():

            self._sessions = []

            self.save()

            return

        try:

            with self._file.open(
                "r",
                encoding="utf-8",
            ) as file:

                data = json.load(file)

            if isinstance(data, list):

                self._sessions = data

            else:

                self._sessions = []

        except (
            json.JSONDecodeError,
            OSError,
        ):

            self._sessions = []

    def save(self):

        self._file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with self._file.open(
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                self._sessions,
                file,
                indent=4,
                ensure_ascii=False,
            )

    # =====================================================
    # ID
    # =====================================================

    def _generate_id(self):

        return (
            max(
                (
                    int(session.get("id", 0))
                    for session in self._sessions
                ),
                default=0,
            )
            + 1
        )

    # =====================================================
    # START
    # =====================================================

    def start_session(
        self,
        subject_id=None,
        task_id=None,
        planned_duration=0,
    ):

        if self._current_session is not None:

            return None

        now = datetime.now()

        self._current_session = {

            "id": self._generate_id(),

            "subject_id": subject_id,

            "task_id": task_id,

            "planned_duration": int(
                planned_duration
            ),

            "actual_duration": 0,

            "started_at": now.isoformat(),

            "finished_at": None,

            "date": now.date().isoformat(),

            "status": "in_progress",
        }

        self.session_started.emit(
            self._current_session.copy()
        )

        return self._current_session.copy()

    # =====================================================
    # CURRENT
    # =====================================================

    def current_session(self):

        if self._current_session is None:

            return None

        return self._current_session.copy()

    # =====================================================
    # FINISH
    # =====================================================

    def finish_session(self):

        if self._current_session is None:

            return None

        finished = datetime.now()

        self._current_session[
            "finished_at"
        ] = finished.isoformat()

        self._current_session[
            "status"
        ] = "completed"

        started = datetime.fromisoformat(
            self._current_session[
                "started_at"
            ]
        )

        seconds = (
            finished - started
        ).total_seconds()

        self._current_session[
            "actual_duration"
        ] = max(
            1,
            int(seconds // 60)
        )

        finished_session = (
            self._current_session.copy()
        )

        self._sessions.append(
            finished_session
        )

        self.save()

        self._current_session = None

        self.session_completed.emit(
            finished_session
        )

        return finished_session

    # =====================================================
    # CANCEL
    # =====================================================

    def cancel_session(self):

        if self._current_session is None:

            return

        self._current_session = None

    # =====================================================
    # READ
    # =====================================================

    def get_sessions(self):
        #اگر فایل عوض شد دوباره بخون 
        try :
            mtime = self._file.stat().st_mtime
        except OSError :
            mtime = 0 

        if getattr(self , "_last_mtime" , None ) != mtime :
            self.load()
            self._last_mtime = mtime
        return self._sessions.copy()


# =====================================================
# SINGLETON
# =====================================================

_shared_instance = None


def get_session_manager() -> SessionManager:

    global _shared_instance

    if _shared_instance is None:

        _shared_instance = SessionManager()

    return _shared_instance