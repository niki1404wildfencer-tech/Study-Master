from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QFrame, QProgressBar, QPushButton, QDialog, QSpinBox,
)
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor

from widgets.clock import ClockWidget
from widgets.timer.TimerDisplay import TimerDisplay
from widgets.timer.TimerControls import TimerControls
from widgets.timer.SubjectProgressBar import SubjectProgressBar
from widgets.stopwatch import Stopwatch
from managers.enum.TimerState import TimerState
from managers.enum.TimerMode  import TimerMode

from ui.components.card import Card
from ui.styles.styles import (
    card_style,
    DASHBOARD_PAGE_TITLE, DASHBOARD_DAY_LBL, DASHBOARD_NAME_LBL,
    DASHBOARD_TIME_LBL, DASHBOARD_TODO_LBL,
    DASHBOARD_DAILYGOAL, DASHBOARD_PROGRESS, DASHBOARD_EDIT_DAILYGOAL,
    DASHBOARD_TODO_ROW, DASHBOARD_TODO_ROW_HOVER,
    DASHBOARD_TODO_TASK_NAME, DASHBOARD_TODO_TASK_NAME_DONE,
    DASHBOARD_TODO_VIEW_ALL, DASHBOARD_TODO_CHECKBOX_EMPTY,
    DASHBOARD_TODO_EMPTY,
    DASHBOARD_GOAL_BAR,
    dashboard_todo_checkbox_done,
    dashboard_todo_stripe,
    dashboard_subject_chip,
    DIALOG_STYLE,
    COMBO_BOX,
    NOTE_DIALOG_HEADER,
    NOTE_FORM_LABEL,
    DIALOG_CANCEL_BTN,
    Add_btn,
)
from ui.styles.spacing import *

from managers.CalendarManager import get_calendar_manager
from managers.TaskManager import TaskManager
from managers.SubjectManager import SubjectManager
from managers.SettingsManager import get_settings_manager
from managers.SessionManager import get_session_manager
from managers.TimerManager import TimerManager
from managers.enum.TimerState import TimerState

from assets.icon.icon import EDIT

from datetime import datetime, date


# ═══════════════════════════════════════════════════════
# Priority colors (mirror PlannerPage)
# ═══════════════════════════════════════════════════════
PRIORITY_COLORS = {
    "critical": "#EF4444",
    "high":     "#F97316",
    "medium":   "#FACC15",
    "low":      "#22C55E",
}


def _dot_pixmap(color, size=10):
    pix = QPixmap(size, size)
    pix.fill(Qt.GlobalColor.transparent)
    p = QPainter(pix)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    p.setBrush(QColor(color))
    p.setPen(Qt.PenStyle.NoPen)
    p.drawEllipse(0, 0, size, size)
    p.end()
    return pix


# ═══════════════════════════════════════════════════════
# Upcoming Events
# ═══════════════════════════════════════════════════════
class EventRowWidget(QFrame):
    clicked = Signal(dict)

    def __init__(self, event, parent=None):
        super().__init__(parent)
        self._event_data = event

        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedHeight(34)
        self.setStyleSheet("background: transparent; border: none;")

        rl = QHBoxLayout(self)
        rl.setContentsMargins(4, 2, 4, 2)
        rl.setSpacing(SMALL)

        today = datetime.now().date()
        try:
            d = datetime.strptime(event.get("date", ""), "%Y-%m-%d").date()
            delta = (d - today).days
            day_text = "Today" if delta == 0 else (
                "Tomorrow" if delta == 1 else d.strftime("%b %d")
            )
        except Exception:
            day_text = event.get("date", "")

        day_lbl = QLabel(f"📅  {day_text}")
        day_lbl.setStyleSheet(DASHBOARD_DAY_LBL)
        day_lbl.setFixedWidth(120)

        dot = QLabel()
        dot.setFixedSize(10, 10)
        dot.setStyleSheet(
            f"background: {event.get('color', '#4F7CFF')}; border-radius: 5px;"
        )

        name_lbl = QLabel(event.get("title", "(untitled)"))
        name_lbl.setStyleSheet(DASHBOARD_NAME_LBL)

        rl.addWidget(day_lbl)
        rl.addWidget(dot)
        rl.addWidget(name_lbl, 1)

        if event.get("time"):
            time_lbl = QLabel(event["time"])
            time_lbl.setStyleSheet(DASHBOARD_TIME_LBL)
            rl.addWidget(time_lbl)

    def _apply_style(self, hovered):
        bg = "rgba(79, 124, 255, 0.08)" if hovered else "transparent"
        self.setStyleSheet(
            f"EventRowWidget {{ background: {bg};"
            f" border: none; border-radius: 8px; }}"
        )

    def enterEvent(self, event):
        self._apply_style(True)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._apply_style(False)
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self._event_data)
            event.accept()
            return
        super().mousePressEvent(event)


class UpcomingEventsWidget(QWidget):

    event_selected = Signal(dict)

    def __init__(self):
        super().__init__()
        self.calendar_manager = get_calendar_manager()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(MEDIUM)

        title = QLabel("Upcoming Events")
        title.setStyleSheet(DASHBOARD_PAGE_TITLE)
        layout.addWidget(title)

        self.list_container = QWidget()
        self.list_layout = QVBoxLayout(self.list_container)
        self.list_layout.setContentsMargins(0, 0, 0, 0)
        self.list_layout.setSpacing(XSMALL)
        self.list_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.list_container, 1)

        self.empty_label = QLabel("No upcoming events")
        self.empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.empty_label.setStyleSheet(DASHBOARD_TODO_EMPTY)
        layout.addWidget(self.empty_label)

        self.calendar_manager.event_changed.connect(self.refresh)
        self.refresh()

    def _clear(self):
        while self.list_layout.count():
            item = self.list_layout.takeAt(0)
            w = item.widget()
            if w is not None:
                w.deleteLater()

    def refresh(self):
        self._clear()
        events = self.calendar_manager.get_upcoming_events(days=7)

        if not events:
            self.empty_label.setVisible(True)
            return
        self.empty_label.setVisible(False)

        for ev in events[:6]:
            row = EventRowWidget(ev)
            row.clicked.connect(self.event_selected.emit)
            self.list_layout.addWidget(row)


# ═══════════════════════════════════════════════════════
# To-Do
# ═══════════════════════════════════════════════════════
class ToDoRowWidget(QFrame):

    toggled = Signal(int, bool)
    clicked = Signal(int)

    def __init__(self, task, subject=None, parent=None):
        super().__init__(parent)
        self._task = task
        self._completed = bool(task.get("completed", False))
        self._priority_color = PRIORITY_COLORS.get(
            task.get("priority", "medium"), "#FACC15"
        )

        self.setObjectName("dashTaskRow")
        self.setFixedHeight(40)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        outer = QHBoxLayout(self)
        outer.setContentsMargins(0, 0, MEDIUM, 0)
        outer.setSpacing(0)

        stripe = QFrame()
        stripe.setFixedWidth(4)
        stripe.setStyleSheet(dashboard_todo_stripe(self._priority_color))
        outer.addWidget(stripe)

        wrap = QWidget()
        wrap.setStyleSheet("background: transparent;")
        outer.addWidget(wrap, 1)

        row = QHBoxLayout(wrap)
        row.setContentsMargins(MEDIUM, 0, 0, 0)
        row.setSpacing(SMALL)

        self.check_btn = QPushButton()
        self.check_btn.setFixedSize(20, 20)
        self.check_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.check_btn.clicked.connect(self._on_check)
        row.addWidget(self.check_btn)
        self._refresh_check_style()

        dot = QLabel()
        dot.setPixmap(_dot_pixmap(self._priority_color, 8))
        dot.setFixedSize(8, 8)
        row.addWidget(dot)

        self.name_lbl = QLabel(task.get("name", "(untitled)"))
        self.name_lbl.setStyleSheet(self._name_style())
        row.addWidget(self.name_lbl, 1)

        if subject:
            chip = QLabel(subject["name"])
            chip.setStyleSheet(
                dashboard_subject_chip(subject.get("color", "#4F7CFF"))
            )
            row.addWidget(chip)

        self.setStyleSheet(DASHBOARD_TODO_ROW)

    def _name_style(self):
        if self._completed:
            return DASHBOARD_TODO_TASK_NAME_DONE
        return DASHBOARD_TODO_TASK_NAME

    def _refresh_check_style(self):
        if self._completed:
            self.check_btn.setText("✓")
            self.check_btn.setStyleSheet(
                dashboard_todo_checkbox_done(self._priority_color)
            )
        else:
            self.check_btn.setText("")
            self.check_btn.setStyleSheet(DASHBOARD_TODO_CHECKBOX_EMPTY)

    def _on_check(self):
        self._completed = not self._completed
        self._refresh_check_style()
        self.name_lbl.setStyleSheet(self._name_style())
        self.toggled.emit(self._task["id"], self._completed)

    def enterEvent(self, event):
        self.setStyleSheet(DASHBOARD_TODO_ROW_HOVER)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setStyleSheet(DASHBOARD_TODO_ROW)
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self._task["id"])
            event.accept()
            return
        super().mousePressEvent(event)


class ToDoListWidget(QWidget):

    task_clicked = Signal(int)
    open_planner = Signal()

    def __init__(self):
        super().__init__()

        self.task_manager = TaskManager()
        self.subject_manager = SubjectManager()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(MEDIUM)

        header = QHBoxLayout()
        header.setSpacing(SMALL)

        title = QLabel("To-Do List")
        title.setStyleSheet(DASHBOARD_TODO_LBL)
        header.addWidget(title)
        header.addStretch()

        self.view_all_btn = QPushButton("View all  →")
        self.view_all_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.view_all_btn.setStyleSheet(DASHBOARD_TODO_VIEW_ALL)
        self.view_all_btn.clicked.connect(self.open_planner.emit)
        header.addWidget(self.view_all_btn)

        layout.addLayout(header)

        self.list_container = QWidget()
        self.list_layout = QVBoxLayout(self.list_container)
        self.list_layout.setContentsMargins(0, 0, 0, 0)
        self.list_layout.setSpacing(XSMALL)
        self.list_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.list_container, 1)

        self.empty_label = QLabel("No tasks yet")
        self.empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.empty_label.setStyleSheet(DASHBOARD_TODO_EMPTY)
        layout.addWidget(self.empty_label)

        self.task_manager.task_changed.connect(self.refresh)
        self.subject_manager.subject_changed.connect(self.refresh)
        self.refresh()

    def _clear(self):
        while self.list_layout.count():
            item = self.list_layout.takeAt(0)
            w = item.widget()
            if w is not None:
                w.deleteLater()

    def refresh(self):
        self._clear()

        tasks = self.task_manager.get_tasks_by_priority(None)[:6]

        if not tasks:
            self.empty_label.setVisible(True)
            return
        self.empty_label.setVisible(False)

        subjects = {s["id"]: s for s in self.subject_manager.get_subjects()}

        for task in tasks:
            subject = subjects.get(task.get("subject_id"))
            row = ToDoRowWidget(task, subject=subject)
            row.toggled.connect(self._on_toggled)
            row.clicked.connect(self.task_clicked.emit)
            self.list_layout.addWidget(row)

    def _on_toggled(self, task_id, completed):
        self.task_manager.set_completed(task_id, completed)


# ═══════════════════════════════════════════════════════
# Daily Goal Dialog
# ═══════════════════════════════════════════════════════
class DailyGoalDialog(QDialog):

    def __init__(self, parent=None, current_minutes=60):
        super().__init__(parent)
        self.setWindowTitle("Daily Goal")
        self.setModal(True)
        self.resize(420, 300)
        self.setMinimumSize(400, 280)
        self.setStyleSheet(DIALOG_STYLE)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(LARGE, LARGE, LARGE, LARGE)
        layout.setSpacing(MEDIUM)

        header = QLabel("Daily Goal")
        header.setStyleSheet(NOTE_DIALOG_HEADER)
        layout.addWidget(header)

        label = QLabel("Minutes per day")
        label.setStyleSheet(NOTE_FORM_LABEL)
        layout.addWidget(label)

        self.spin = QSpinBox()
        self.spin.setStyleSheet(COMBO_BOX)
        self.spin.setRange(1, 1440)
        self.spin.setValue(max(1, int(current_minutes)))
        self.spin.setSuffix(" min")
        self.spin.setFixedHeight(48)
        layout.addWidget(self.spin)

        layout.addStretch()

        row = QHBoxLayout()
        row.setSpacing(MEDIUM)
        row.addStretch()

        cancel = QPushButton("Cancel")
        cancel.setObjectName("dialogCancelBtn")
        cancel.setFixedSize(140, 56)
        cancel.setStyleSheet(DIALOG_CANCEL_BTN)
        cancel.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel.clicked.connect(self.reject)

        save = QPushButton("Save")
        save.setFixedSize(140, 56)
        save.setStyleSheet(Add_btn)
        save.setCursor(Qt.CursorShape.PointingHandCursor)
        save.clicked.connect(self._on_save)

        row.addWidget(cancel)
        row.addWidget(save)
        layout.addLayout(row)

    def _on_save(self):
        self._value = self.spin.value()
        self.accept()

    def value(self):
        return getattr(self, "_value", None)


# ═══════════════════════════════════════════════════════
# Daily Goal Bar (real, connected, singleton-safe)
# ═══════════════════════════════════════════════════════
class DailyGoalBar(QFrame):

    def __init__(self):
        super().__init__()
        self.settings_manager = get_settings_manager()
        self.session_manager = get_session_manager()
        self.subject_manager = SubjectManager()

        self.setObjectName("dashGoalBar")
        self.setAttribute(Qt.WidgetAttribute.WA_Hover, True)
        self.setStyleSheet(DASHBOARD_GOAL_BAR)
        self.setFixedHeight(80)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(MEDIUM, SMALL, MEDIUM, SMALL)
        layout.setSpacing(MEDIUM)

        self.label = QLabel("Daily Goal:  0 / 0 min")
        self.label.setStyleSheet(DASHBOARD_DAILYGOAL)

        # Same widget the timer page uses — colored segments per subject
        self.progress = SubjectProgressBar()
        self.progress.setFixedHeight(26)

        self.edit_btn = QPushButton()
        self.edit_btn.setIcon(QIcon(str(EDIT)))
        self.edit_btn.setIconSize(QSize(18, 18))
        self.edit_btn.setFixedSize(40, 40)
        self.edit_btn.setStyleSheet(DASHBOARD_EDIT_DAILYGOAL)
        self.edit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.edit_btn.setToolTip("Edit daily goal")
        self.edit_btn.clicked.connect(self.edit_goal)

        layout.addWidget(self.label)
        layout.addWidget(self.progress, 1)
        layout.addWidget(self.edit_btn)

        # Live sync
        self.settings_manager.settings_changed.connect(self.refresh)
        self.session_manager.session_completed.connect(self._on_session_completed)
        self.subject_manager.subject_changed.connect(self.refresh)

        self.refresh()

    # ─────────────────────────────────────
    def _on_session_completed(self, _session):
        self.refresh()

    def _get_today_by_subject(self):
        """Return {subject_id: minutes} for today's sessions."""
        today = date.today().isoformat()
        result = {}
        for s in self.session_manager.get_sessions():
            if s.get("date") != today:
                continue
            minutes = int(s.get("actual_duration", 0))
            if minutes <= 0:
                continue
            sid = s.get("subject_id")
            key = sid if sid is not None else -1
            result[key] = result.get(key, 0) + minutes
        return result

    def refresh(self):
        goal = self.settings_manager.get_daily_goal_minutes()
        studied_by_subject = self._get_today_by_subject()
        total = sum(studied_by_subject.values())

        self.label.setText(f"Daily Goal:  {total} / {goal} min")

        color_map = {
            s["id"]: s["color"]
            for s in self.subject_manager.get_subjects()
        }

        self.progress.set_data(studied_by_subject, goal, color_map)

    def edit_goal(self):
        current = self.settings_manager.get_daily_goal_minutes()
        dialog = DailyGoalDialog(self, current)
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return
        value = dialog.value()
        if value is None:
            return
        self.settings_manager.set_daily_goal_minutes(value)
# ═══════════════════════════════════════════════════════
# Dashboard Page
# ═══════════════════════════════════════════════════════
class DashboardPage(QWidget):

    event_selected = Signal(dict)
    task_clicked = Signal(int)
    open_planner = Signal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Study Master")

        self.timer_manager = TimerManager()

        self.setup_ui()
        self.connect_timer()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(LARGE, LARGE, LARGE, LARGE)
        main_layout.setSpacing(MEDIUM)

        row1 = QHBoxLayout()
        row1.setSpacing(MEDIUM)

        TOP_H = 300

        clock_card = Card()
        clock_card.setFixedHeight(TOP_H)
        clock_card.add_widget(ClockWidget(clock_size=48, date_size=13))

        timer_card = Card()
        timer_card.setFixedHeight(TOP_H)
        self.dash_timer_display = TimerDisplay(
            font_size=40, status_size=15, auto_fit=True
        )
        self.dash_timer_controls = TimerControls()
        timer_card.card_layout.addWidget(self.dash_timer_display , 1)
        timer_card.card_layout.addWidget(self.dash_timer_controls , 0)

        stopwatch_card = Card()
        stopwatch_card.setFixedHeight(TOP_H)
        stopwatch_card.add_widget(Stopwatch(font_size=55))

        row1.addWidget(clock_card, 1)
        row1.addWidget(timer_card, 1)
        row1.addWidget(stopwatch_card, 1)

        main_layout.addLayout(row1)

        row2 = QHBoxLayout()
        row2.setSpacing(MEDIUM)

        events_card = Card()
        events_card.setMinimumHeight(0)
        self.upcoming_events = UpcomingEventsWidget()
        self.upcoming_events.event_selected.connect(self.event_selected.emit)
        events_card.add_widget(self.upcoming_events)

        todo_card = Card()
        todo_card.setMinimumHeight(0)
        self.todo_list = ToDoListWidget()
        self.todo_list.task_clicked.connect(self.task_clicked.emit)
        self.todo_list.open_planner.connect(self.open_planner.emit)
        todo_card.add_widget(self.todo_list)

        row2.addWidget(events_card, 1)
        row2.addWidget(todo_card, 1)

        main_layout.addLayout(row2, 1)

        self.daily_goal_bar = DailyGoalBar()
        main_layout.addWidget(self.daily_goal_bar)

    def connect_timer(self):
        self.dash_timer_display.set_time(self.timer_manager.format_time())
        self._on_timer_state(self.timer_manager.state)

        self.timer_manager.time_changed.connect(self.dash_timer_display.set_time)
        self.timer_manager.state_changed.connect(self._on_timer_state)

        # When a focus session fully completes, show "Session Completed"
        # on the dashboard display too (matches the timer page behaviour).
        self.timer_manager.finished.connect(
            lambda _: self.dash_timer_display.finish()
        )

        self.dash_timer_controls.start_requested.connect(self.timer_manager.start)
        self.dash_timer_controls.pause_requested.connect(self.timer_manager.pause)
        self.dash_timer_controls.resume_requested.connect(self.timer_manager.resume)
        self.dash_timer_controls.reset_requested.connect(self.timer_manager.restart)
        self.dash_timer_controls.skip_requested.connect(self.timer_manager.skip)

    def _on_timer_state(self, state):
        if state == TimerState.STOPPED:
            self.dash_timer_controls.set_start()
            self.dash_timer_display.reset()
        elif state == TimerState.PAUSED:
            self.dash_timer_controls.set_paused()
            self.dash_timer_display.pause()
        elif state == TimerState.RUNNING:
            self.dash_timer_controls.set_running()
            if self.timer_manager.current_mode == TimerMode.FOCUS:
                self.dash_timer_display.start_focus()
            else:
                self.dash_timer_display.start_break()