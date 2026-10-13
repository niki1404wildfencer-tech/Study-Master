from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QDialog
)
from PySide6.QtCore import Qt

from widgets.calendar.calendar import CalendarWidget
from widgets.calendar.EventInput import AddEvent , EventViewer
from widgets.calendar.DayEventsPopup import DayEventsPopup

from managers.CalendarManager import get_calendar_manager
from managers.SubjectManager import SubjectManager
from managers.TaskManager import TaskManager

from ui.components.card import Card
from ui.styles.styles import (
    menu_label_style, selector_shared, CALENDAR_TOGGLE_ACTIVE, Add_btn,
)
from ui.styles.spacing import LARGE, MEDIUM, SMALL


class CalendarPage(QWidget):

    def __init__(self):
        super().__init__()

        self.calendar_type = "gregorian"
        self.subject_manager = SubjectManager()
        self.task_manager = TaskManager()
        self.calendar_manager = get_calendar_manager()
        self.on_show_all_events = None

        self.setup_ui()
        self.connect_signals()
        self._update_button_states()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(LARGE, LARGE, LARGE, LARGE)
        layout.setSpacing(MEDIUM)

        self.title = QLabel("Calendar")
        self.title.setStyleSheet(menu_label_style)
        layout.addWidget(self.title)

        controls_row = QHBoxLayout()
        controls_row.setSpacing(SMALL)

        self.gregorian_btn = QPushButton("Gregorian")
        self.gregorian_btn.setFixedHeight(46)
        self.gregorian_btn.setMinimumWidth(120)
        self.gregorian_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        self.shamsi_btn = QPushButton("Persian")
        self.shamsi_btn.setFixedHeight(46)
        self.shamsi_btn.setMinimumWidth(120)
        self.shamsi_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        self.all_events_btn = QPushButton("All My Events")
        self.all_events_btn.setFixedHeight(50)
        self.all_events_btn.setMinimumWidth(180)
        self.all_events_btn.setStyleSheet(selector_shared)
        self.all_events_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        self.add_event_btn = QPushButton("+ Add Event")
        self.add_event_btn.setFixedHeight(50)
        self.add_event_btn.setMinimumWidth(180)
        self.add_event_btn.setStyleSheet(Add_btn)
        self.add_event_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        controls_row.addWidget(self.gregorian_btn)
        controls_row.addWidget(self.shamsi_btn)
        controls_row.addStretch()
        controls_row.addWidget(self.all_events_btn)
        controls_row.addWidget(self.add_event_btn)
        layout.addLayout(controls_row)

        self.calendar_card = Card()
        self.calendar_card.setMinimumHeight(0)

        self.calendar_widget = CalendarWidget(calendar_type="gregorian")
        self.calendar_widget.day_clicked.connect(self._on_day_clicked)
        self.calendar_widget.event_clicked.connect(self._on_event_clicked)
        self.calendar_card.add_widget(self.calendar_widget)

        layout.addWidget(self.calendar_card, 1)

    def connect_signals(self):
        self.gregorian_btn.clicked.connect(lambda: self._set_type("gregorian"))
        self.shamsi_btn.clicked.connect(lambda: self._set_type("shamsi"))
        self.add_event_btn.clicked.connect(self._add_event)
        self.all_events_btn.clicked.connect(self._show_all_events)

    def _set_type(self, cal_type):
        if cal_type == self.calendar_type:
            return
        self.calendar_type = cal_type
        self.calendar_widget.set_calendar_type(cal_type)
        self._update_button_states()

    def _update_button_states(self):
        if self.calendar_type == "gregorian":
            self.gregorian_btn.setStyleSheet(CALENDAR_TOGGLE_ACTIVE)
            self.shamsi_btn.setStyleSheet(selector_shared)
        else:
            self.gregorian_btn.setStyleSheet(selector_shared)
            self.shamsi_btn.setStyleSheet(CALENDAR_TOGGLE_ACTIVE)

    def _show_all_events(self):
        if self.on_show_all_events is not None:
            self.on_show_all_events()

    def _add_event(self):
        from datetime import datetime
        self._open_event_dialog(date_str=datetime.now().date().isoformat())

    def _open_event_dialog(self, date_str=None, existing_event=None):
        dialog = AddEvent(
            title="Edit Event" if existing_event else "Add Event",
            date_str=date_str or "",
            subject_manager=self.subject_manager,
            task_manager=self.task_manager,
            parent=self,
            calendar_type=self.calendar_type,
            existing_event=existing_event,
        )
        result = dialog.exec()

        if result == QDialog.DialogCode.Rejected:
            return

        if result == 2:
            if existing_event is not None:
                self.calendar_manager.delete_event(existing_event["id"])
            return

        data = dialog.value()
        if existing_event is None:
            self.calendar_manager.add_event(**data)
        else:
            self.calendar_manager.update_event(existing_event["id"], **data)


    def _on_day_clicked(self, date_str, events):
        popup = DayEventsPopup(
            date_str=date_str, events=events,
            calendar_type=self.calendar_type, parent=self,
        )

        def _on_pick(ev):
            full = self.calendar_manager.get_event(ev.get("id")) or ev
            subject = None
            if full.get("subject_id") is not None:
                subject = self.subject_manager.get_subject(full["subject_id"])
            task = None
            if full.get("task_id") is not None:
                task = self.task_manager.get_task(full["task_id"])

            viewer = EventViewer(full, subject=subject, task=task, parent=self)
            viewer.edit_requested.connect(
                lambda e2: self._open_event_dialog(
                    date_str=e2.get("date", ""), existing_event=e2,
                )
            )
            viewer.exec()

        popup.edit_requested.connect(_on_pick)
        popup.add_requested.connect(
            lambda ds: self._open_event_dialog(date_str=ds)
        )
        popup.exec()
    def _on_event_clicked(self, event):
        full = self.calendar_manager.get_event(event.get("id")) or event

        subject = None
        if full.get("subject_id") is not None:
            subject = self.subject_manager.get_subject(full["subject_id"])

        task = None
        if full.get("task_id") is not None:
            task = self.task_manager.get_task(full["task_id"])

        viewer = EventViewer(full, subject=subject, task=task, parent=self)
        viewer.edit_requested.connect(
            lambda ev: self._open_event_dialog(
                date_str=ev.get("date", ""), existing_event=ev,
            )
        )
        viewer.exec()