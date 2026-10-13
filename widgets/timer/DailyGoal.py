from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QLabel, QSpinBox, QVBoxLayout

from managers.SettingsManager import get_settings_manager
from ui.styles.styles import COMBO_BOX, selector_label_style


class DailyGoal(QWidget):
    goal_changed = Signal(int)
    progress_updated = Signal(float)

    def __init__(self, settings_manager=None, parent=None):
        super().__init__(parent)
        self.settings_manager = settings_manager or get_settings_manager()
        self.goal_minutes = self.settings_manager.get_daily_goal_minutes()
        self.study_minutes = 0

        self.setup_ui()
        self.connect_signals()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        self.title_label = QLabel("Daily Goal")
        self.title_label.setStyleSheet(selector_label_style)

        self.goal_spin = QSpinBox()
        self.goal_spin.setRange(0, 24 * 60)
        self.goal_spin.setSuffix(" min")
        self.goal_spin.setMinimumHeight(42)
        self.goal_spin.setStyleSheet(COMBO_BOX)
        self.goal_spin.setValue(self.goal_minutes)

        layout.addWidget(self.title_label)
        layout.addWidget(self.goal_spin)

    def connect_signals(self):
        self.goal_spin.valueChanged.connect(self.on_spin_changed)
        self.settings_manager.settings_changed.connect(self.on_settings_changed)

    def on_spin_changed(self, value):
        if self.settings_manager.set_daily_goal_minutes(value):
            self.goal_minutes = value
            self.goal_changed.emit(value)
            self.progress_updated.emit(self.get_progress())

    def on_settings_changed(self):
        new_value = self.settings_manager.get_daily_goal_minutes()
        if new_value == self.goal_minutes:
            return
        self.goal_minutes = new_value
        self.goal_spin.blockSignals(True)
        self.goal_spin.setValue(new_value)
        self.goal_spin.blockSignals(False)
        # Notify downstream listeners (progress bar, stats, etc.)
        self.goal_changed.emit(new_value)
        self.progress_updated.emit(self.get_progress())

    def set_study_minutes(self, minutes):
        self.study_minutes = minutes
        self.progress_updated.emit(self.get_progress())

    def get_progress(self):
        if self.goal_minutes <= 0:
            return 0.0
        return min(1.0, self.study_minutes / self.goal_minutes)