from PySide6.QtCore import QPropertyAnimation, QSize, QPoint
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QFrame, QPushButton, QSizePolicy
)
from ui.components.card import Card
from managers.enum.TimerState import TimerState
from widgets.timer.TimerControls import TimerControls
from widgets.timer.SessionInfoCard import SessionInfoCard
from widgets.timer.TimerDisplay import TimerDisplay
from widgets.timer.SessionSetUp import SessionSetUp
from managers.SubjectManager import SubjectManager
from managers.TaskManager import TaskManager
from managers.TimerManager import TimerManager
from managers.StatsManager import StatisticsManager
from managers.SessionManager import SessionManager
from managers.SettingsManager import SettingsManager
from ui.styles.spacing import *
from ui.styles.styles import SESSION_BUTTON
from ui.animations.easing import SMOOTH
from assets.icon.icon import EXPAND_DOWN, EXPAND_UP


class TimerPage(QWidget):
    def __init__(self):
        super().__init__()
        self.time_display = TimerDisplay()
        self.timer_control = TimerControls()
        self.session_card = SessionInfoCard()
        self.session_setup = SessionSetUp()

        self.subject_manager = SubjectManager()
        self.task_manager = TaskManager()
        self.manager = TimerManager()
        self.session_manager = self.manager.session_manager
        self.settings_manager = SettingsManager()
        self.stats_manager = StatisticsManager()
        self.stats_manager.set_sessions(self.session_manager.get_sessions())
        self.stats_manager.set_daily_goal(self.settings_manager.get_daily_goal_minutes())

        self.overlay_visible = False
        self._anim = None

        self.setup_ui()
        self.connect_manager()
        self.connect_signals()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(XSMALL)

        self.toggle_btn = QPushButton("Session Setup")
        self.toggle_btn.setIcon(QIcon(str(EXPAND_DOWN)))
        self.toggle_btn.setIconSize(QSize(30, 30))
        self.toggle_btn.setStyleSheet(SESSION_BUTTON)
        self.toggle_btn.setFixedHeight(60)
        self.toggle_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        main_layout.addWidget(self.toggle_btn)

        timer_card = Card()
        timer_card.setMinimumHeight(0)
        timer_card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        timer_card.layout().addWidget(self.time_display)
        timer_card.layout().addWidget(self.timer_control)
        main_layout.addWidget(timer_card, stretch=1)

        session_card = Card()
        session_card.layout().addWidget(self.session_card)
        main_layout.addWidget(session_card)

        self.overlay = QFrame(self)
        self.overlay.setStyleSheet(
            "background-color: rgba(255,255,255,0.98);"
            "border: none;"
        )
        overlay_layout = QVBoxLayout(self.overlay)
        overlay_layout.setContentsMargins(0, 0, 0, 0)
        overlay_layout.addWidget(self.session_setup)
        self.overlay.hide()

    def connect_signals(self):
        self.timer_control.start_requested.connect(self.manager.start)
        self.timer_control.pause_requested.connect(self.manager.pause)
        self.timer_control.resume_requested.connect(self.manager.resume)
        self.timer_control.reset_requested.connect(self.manager.restart)
        self.timer_control.skip_requested.connect(self.manager.skip)

        self.session_setup.duration_sel.duration_changed.connect(self.manager.set_duration_minutes)
        self.session_setup.sound_selector.currentTextChanged.connect(
            self.manager.set_completion_sound
        )


        self.session_setup.subject_sel.subject_changed.connect(self.session_setup.task_sel.set_subject)
        self.session_setup.subject_sel.subject_changed.connect(self.manager.set_subject)
        self.session_setup.subject_sel.subject_changed.connect(
            lambda subject_id: self.manager.set_subject_name(
                self.session_setup.subject_sel.current_subject_name()
            )
        )
        self.session_setup.subject_sel.subject_changed.connect(
            lambda _: self.update_session_info()
        )

        self.session_setup.task_sel.task_changed.connect(self.manager.set_task)
        self.session_setup.task_sel.task_changed.connect(
            lambda task_id: self.manager.set_task_name(
                self.session_setup.task_sel.current_task_name()
            )
        )
        self.session_setup.task_sel.task_changed.connect(
            lambda _: self.update_session_info()
        )

        self.toggle_btn.clicked.connect(self.toggle_overlay)
        self.session_setup.close_requested.connect(self.hide_overlay)
        self.manager.state_changed.connect(self.on_state_changed)
        self.manager.finished.connect(lambda _: self.timer_control.set_start())
        self.session_setup.daily_goal.goal_changed.connect(self.refresh_progress)
        self.session_setup.subject_sel.subject_changed.connect(self.refresh_progress)
        self.manager.finished.connect(self.on_session_finished)

    def on_session_finished(self, session):
        if session is None:
            return

        self.stats_manager.set_sessions(
            self.session_manager.get_sessions()
        )

        duration = session.get("actual_duration", 0)
        goal_data = self.stats_manager.get_daily_goal_data()
    
        from ui.components.MessageBox import ThemedMessageBox

        if goal_data["completed"]:
            # 🎉 هدف روزانه کامل شد
            ThemedMessageBox.success(
                self,
                "🎉 Daily Goal Achieved!",
                f"Amazing work!\n\n"
                f"You've completed your daily goal of "
                f"{int(goal_data['goal_minutes'])} minutes.\n\n"
                f"Total studied today: "
                f"{int(goal_data['studied_minutes'])} min"
            )
        else:
            # ✅ سشن عادی
            studied = int(goal_data["studied_minutes"])
            goal = int(goal_data["goal_minutes"])
            remaining = max(0, goal - studied)
            ThemedMessageBox.success(
                self,
                "Session Completed",
                f"Great job!\n\n"
                f"You studied for {duration} minutes.\n"
                f"Progress: {studied} / {goal} min\n"
                f"Only {remaining} min left to reach your goal!"
            )

        self.refresh_progress()
        self.refresh_progress()
    def on_state_changed(self, state):
        if state == TimerState.STOPPED:
            self.timer_control.set_start()
        elif state == TimerState.PAUSED:
            self.timer_control.set_paused()
        elif state == TimerState.RUNNING:
            self.timer_control.set_running()
    def connect_manager(self):
        self.manager.set_display(self.time_display)
        self.manager.set_controls(self.timer_control)
        self.manager.set_session_card(self.session_card)

        self.manager.set_duration_minutes(self.session_setup.duration_sel.current_duration())

        self.session_setup.set_subject_manager(self.subject_manager)
        self.session_setup.set_task_manager(self.task_manager)

        subject_id = self.session_setup.subject_sel.current_subject_id()
        if subject_id is not None:
            self.session_setup.task_sel.set_subject(subject_id)
            self.manager.set_subject(subject_id)
            self.manager.set_subject_name(self.session_setup.subject_sel.current_subject_name())

        task_id = self.session_setup.task_sel.current_task_id()
        if task_id is not None:
            self.manager.set_task(task_id)
            self.manager.set_task_name(self.session_setup.task_sel.current_task_name())

        self.update_session_info()
        self.refresh_progress()

    def update_session_info(self):
        subject_name = self.session_setup.subject_sel.current_subject_name()
        task_name = self.session_setup.task_sel.current_task_name()
        duration = f"{self.session_setup.duration_sel.current_duration()} min"
        status = "Ready to start" if subject_name != "" else "No session selected"
        self.session_card.update_session(subject_name, task_name, duration, status)

    def toggle_overlay(self):
        if self.overlay_visible:
            self.hide_overlay()
        else:
            self.show_overlay()

    def show_overlay(self):
        if self.overlay_visible:
            return
        self.overlay_visible = True
        self.overlay.show()
        self.overlay.raise_()
        self.update_overlay_geometry()
        self.toggle_btn.setIcon(QIcon(str(EXPAND_UP)))
        self._animate_overlay(show=True)

    def hide_overlay(self):
        if not self.overlay_visible:
            return
        self.overlay_visible = False
        self.toggle_btn.setIcon(QIcon(str(EXPAND_DOWN)))
        self._animate_overlay(show=False)

    def _animate_overlay(self, show):
        if self._anim:
            self._anim.stop()
            self._anim.deleteLater()

        start_y = -self.overlay.height() if show else 0
        end_y = 0 if show else -self.overlay.height()

        anim = QPropertyAnimation(self.overlay, b"pos")
        anim.setDuration(300)
        anim.setStartValue(QPoint(self.overlay.x(), start_y))
        anim.setEndValue(QPoint(self.overlay.x(), end_y))
        anim.setEasingCurve(SMOOTH)
        if not show:
            anim.finished.connect(self.overlay.hide)
        self._anim = anim
        anim.start()

    def update_overlay_geometry(self):
        if self.overlay_visible:
            content_height = self.session_setup.sizeHint().height()
            half_page = int(self.height() * 0.7)
            height = min(content_height + 20, half_page)
            height = max(height, self.toggle_btn.height() + 20)
            self.overlay.setGeometry(0, 0, self.width(), height)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_overlay_geometry()

    def refresh_progress(self, *args):
        goal = self.session_setup.daily_goal.goal_minutes
        self.stats_manager.set_daily_goal(goal)
        studied_by_subject = self.stats_manager.get_today_study_by_subject()
        color_map = {}
        for subject in self.subject_manager.get_subjects():
            color_map[subject["id"]] = subject["color"]
        self.session_card.set_progress(studied_by_subject, goal, color_map)