from PySide6.QtWidgets import QWidget, QStackedWidget, QHBoxLayout, QDialog

from ui.pages.sidebarPage import Sidebar
from ui.pages.Dashboard_page import DashboardPage
from ui.pages.clockpage import Clockpage
from ui.pages.timerpage import TimerPage
from ui.pages.stopwatchpage import stopwatch
from ui.pages.NotePage import NotesPage
from ui.pages.StatsPage import StatsPage
from ui.pages.CalendarPage import CalendarPage
from ui.pages.PlannerPage import PlannerPage
from ui.pages.AllEventPage import AllEventsPage
from ui.styles.styles import main_window_style
from ui.animations.animation_manager import AnimationManager
from managers.ReminderServiceManager import ReminderService
from widgets.calendar.EventInput import AddEvent , EventViewer
from widgets.AddTaskDialog import AddTaskDialog                 # ← NEW
from ui.components.MessageBox import ThemedMessageBox
from ui.pages.AboutPage import AboutPage


class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Study Master")
        self.resize(1000, 850)
        self.setMinimumSize(800, 700)
        self.setStyleSheet(main_window_style)

        self.stack = QStackedWidget()
        self.sidebar = Sidebar()
        self.clock_page = Clockpage()
        self.dashboard_page = DashboardPage()
        self.timer_page = TimerPage()
        self.stopwatch_page = stopwatch()
        self.note_page = NotesPage()
        self.stats_page = StatsPage()
        self.calendar_page = CalendarPage()
        self.planner_page = PlannerPage()
        self.all_events_page = AllEventsPage()
        self.about_page = AboutPage()

        self.setup_ui()

        self.reminder_service = ReminderService(self)
        self.reminder_service.reminder_fired.connect(self._on_reminder_fired)
        self.reminder_service.start()

    def setup_ui(self):
        main_layout = QHBoxLayout()

        for page in (
            self.dashboard_page, self.clock_page, self.timer_page,
            self.stopwatch_page, self.note_page, self.stats_page,
            self.calendar_page, self.all_events_page, self.planner_page , self.about_page
        ):
            self.stack.addWidget(page)

        self.stack.setCurrentIndex(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.stack, 1)

        self.sidebar.clock_btn.clicked.connect(lambda: self.show_page(self.clock_page))
        self.sidebar.timer_btn.clicked.connect(lambda: self.show_page(self.timer_page))
        self.sidebar.stopwatch_btn.clicked.connect(lambda: self.show_page(self.stopwatch_page))
        self.sidebar.notes_btn.clicked.connect(lambda: self.show_page(self.note_page))
        self.sidebar.Statistics_btn.clicked.connect(lambda: self.show_page(self.stats_page))
        self.sidebar.calendar_btn.clicked.connect(lambda: self.show_page(self.calendar_page))
        self.sidebar.planner_btn.clicked.connect(lambda: self.show_page(self.planner_page))
        self.sidebar.about_btn.clicked.connect(lambda: self.show_page(self.about_page))
        self.sidebar.dashboard_btn.clicked.connect(lambda: self.show_page(self.dashboard_page))

        # Calendar <-> All Events
        self.calendar_page.on_show_all_events = self.show_all_events
        self.dashboard_page.event_selected.connect(self._view_event)
        self.all_events_page.back_requested.connect(
            lambda: self.show_page(self.calendar_page)
        )
        self.all_events_page.event_selected.connect(self._view_event)

        # Dashboard To-Do <-> Planner
        self.dashboard_page.task_clicked.connect(self._edit_task)
        self.dashboard_page.open_planner.connect(
            lambda: self.show_page(self.planner_page)
        )

        self.setLayout(main_layout)

    def show_page(self, page):
        AnimationManager.transition_page(self.stack, page)

    def show_all_events(self):
        self.all_events_page.refresh()
        AnimationManager.transition_page(self.stack, self.all_events_page)
    def _view_event(self, event):
        full = self.calendar_page.calendar_manager.get_event(event.get("id")) or event

        subject = None
        if full.get("subject_id") is not None:
            subject = self.calendar_page.subject_manager.get_subject(full["subject_id"])

        task = None
        if full.get("task_id") is not None:
            task = self.calendar_page.task_manager.get_task(full["task_id"])

        viewer = EventViewer(full, subject=subject, task=task, parent=self)
        viewer.edit_requested.connect(self._edit_event)
        viewer.exec()
    def _edit_event(self, event):
        dialog = AddEvent(
            title="Edit Event",
            date_str=event.get("date", ""),
            subject_manager=self.calendar_page.subject_manager,
            task_manager=self.calendar_page.task_manager,
            parent=self,
            existing_event=event,
            calendar_type=self.calendar_page.calendar_type,
        )
        result = dialog.exec()
        if result == QDialog.DialogCode.Rejected:
            return

        mgr = self.calendar_page.calendar_manager
        if result == 2:
            mgr.delete_event(event["id"])
        else:
            mgr.update_event(event["id"], **dialog.value())

        self.all_events_page.refresh()

    # ─────────────────────────────────────────
    def _edit_task(self, task_id):
        mgr = self.dashboard_page.todo_list.task_manager
        task = mgr.get_task(task_id)
        if task is None:
            return

        dialog = AddTaskDialog(parent=self, task=task)
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        data = dialog.value()
        if not data:
            return

        mgr.update_task(
            task_id=task_id,
            name=data["name"],
            subject_id=data["subject_id"],
            priority=data["priority"],
        )
        # refresh is automatic via task_changed

    def _on_reminder_fired(self, event):
        title = event.get("title", "(untitled)")
        time_str = event.get("time", "")
        details = event.get("details", "")
        msg = f"🔔 Reminder\n\n{title}"
        if time_str:
            msg += f"\nAt {time_str}"
        if details:
            msg += f"\n\n{details}"
        ThemedMessageBox.info(self, "Reminder", msg)