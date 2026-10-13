from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QComboBox, QSpinBox, QDateEdit,
    QWidget, QFrame, QSizePolicy, QScrollArea,
)
from PySide6.QtCore import Qt, QDate

from ui.styles.styles import (
    DIALOG_STYLE, EVENT_DIALOG_HEADER, EVENT_FORM_LABEL,
    EVENT_SAVE_BUTTON, EVENT_CANCEL_BUTTON,
    EVENT_REMOVE_BUTTON, EVENT_ADD_REMINDER_BUTTON,
)
from ui.styles.colors import (
    CARD, BORDER, TEXT, TEXT_SECONDARY, PRIMARY,
)
from ui.styles.fonts import FONT_STACK
from ui.styles.spacing import SMALL, MEDIUM, LARGE

from assets.SoundSystem import SoundManager


WHEN_OPTIONS = [
    ("On the day", "on_day"),
    ("1 day before", "1_day_before"),
    ("1 week before", "1_week_before"),
    ("Custom date", "custom"),
]

SOUND_OPTIONS = list(SoundManager.COMPLETION_SOUNDS.keys())


INPUT_STYLE = f"""
QComboBox, QSpinBox, QDateEdit {{
    background-color: {CARD};
    color: {TEXT};
    border: 1px solid {BORDER};
    border-radius: 10px;
    padding: 4px 8px;
    font-family: {FONT_STACK};
    font-size: 13px;
    font-weight: 600;
    min-height: 26px;
}}
QComboBox:hover, QSpinBox:hover, QDateEdit:hover {{
    border: 1px solid {PRIMARY};
}}
QComboBox:focus, QSpinBox:focus, QDateEdit:focus {{
    border: 2px solid {PRIMARY};
}}
QComboBox::drop-down {{
    border: none;
    width: 22px;
}}
QComboBox QAbstractItemView {{
    background-color: {CARD};
    color: {TEXT};
    border: 1px solid {BORDER};
    border-radius: 8px;
    padding: 4px;
    selection-background-color: {PRIMARY};
    selection-color: white;
}}
QSpinBox::up-button, QSpinBox::down-button {{
    width: 0;
    height: 0;
    border: none;
}}
"""


CALENDAR_STYLE = f"""
QCalendarWidget {{
    background-color: {CARD};
}}
QCalendarWidget QWidget {{
    background-color: {CARD};
    color: {TEXT};
    alternate-background-color: #F5F7FB;
}}
QCalendarWidget QWidget#qt_calendar_navigationbar {{
    background-color: {CARD};
    border-bottom: 1px solid {BORDER};
}}
QCalendarWidget QToolButton {{
    background: transparent;
    color: {TEXT};
    border: none;
    padding: 4px 10px;
    font-family: {FONT_STACK};
    font-size: 13px;
    font-weight: 700;
}}
QCalendarWidget QToolButton:hover {{
    background: rgba(79, 124, 255, 0.12);
    border-radius: 6px;
}}
QCalendarWidget QToolButton::menu-indicator {{
    image: none;
    width: 0;
}}
QCalendarWidget QMenu {{
    background-color: {CARD};
    color: {TEXT};
    border: 1px solid {BORDER};
}}
QCalendarWidget QSpinBox {{
    background-color: {CARD};
    color: {TEXT};
    border: 1px solid {BORDER};
    border-radius: 6px;
    padding: 2px 6px;
    selection-background-color: {PRIMARY};
    selection-color: white;
}}
QCalendarWidget QAbstractItemView {{
    background-color: {CARD};
    color: {TEXT};
    outline: none;
    selection-background-color: {PRIMARY};
    selection-color: white;
}}
QCalendarWidget QAbstractItemView:disabled {{
    color: #9CA3AF;
}}
QCalendarWidget QAbstractItemView::item:hover {{
    background: rgba(79, 124, 255, 0.12);
}}
"""


class ReminderRow(QFrame):

    def __init__(self, on_remove, data=None):
        super().__init__()
        self._on_remove = on_remove

        self.setObjectName("reminderRow")
        self.setStyleSheet(f"""
            QFrame#reminderRow {{
                background: {CARD};
                border: 1px solid {BORDER};
                border-radius: 12px;
            }}
            QFrame#reminderRow:hover {{
                border: 1px solid {PRIMARY};
            }}
        """)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(12, 10, 12, 10)
        outer.setSpacing(8)

        top = QHBoxLayout()
        top.setSpacing(8)

        self.when_combo = QComboBox()
        self.when_combo.setFixedSize(140, 38)
        self.when_combo.setStyleSheet(INPUT_STYLE)
        for label, value in WHEN_OPTIONS:
            self.when_combo.addItem(label, value)

        self.hour = QSpinBox()
        self.hour.setRange(1, 12)
        self.hour.setValue(9)
        self.hour.setFixedSize(62, 38)
        self.hour.setStyleSheet(INPUT_STYLE)
        self.hour.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hour.setButtonSymbols(QSpinBox.ButtonSymbols.NoButtons)

        colon = QLabel(":")
        colon.setFixedWidth(8)
        colon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        colon.setStyleSheet(
            f"color: {TEXT}; font-size: 16px; font-weight: 700;"
            f" background: transparent;"
        )

        self.minute = QSpinBox()
        self.minute.setRange(0, 59)
        self.minute.setFixedSize(62, 38)
        self.minute.setStyleSheet(INPUT_STYLE)
        self.minute.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.minute.setButtonSymbols(QSpinBox.ButtonSymbols.NoButtons)

        self.ampm = QComboBox()
        self.ampm.addItems(["AM", "PM"])
        self.ampm.setFixedSize(72, 38)
        self.ampm.setStyleSheet(INPUT_STYLE)

        self.sound = QComboBox()
        self.sound.addItems(SOUND_OPTIONS)
        self.sound.setFixedHeight(38)
        self.sound.setStyleSheet(INPUT_STYLE)
        self.sound.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )

        remove_btn = QPushButton("✕")
        remove_btn.setFixedSize(32, 32)
        remove_btn.setStyleSheet(EVENT_REMOVE_BUTTON)
        remove_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        remove_btn.setToolTip("Remove this reminder")
        remove_btn.clicked.connect(lambda: self._on_remove(self))

        top.addWidget(self.when_combo)
        top.addWidget(self.hour)
        top.addWidget(colon)
        top.addWidget(self.minute)
        top.addWidget(self.ampm)
        top.addWidget(self.sound, 1)
        top.addWidget(remove_btn)
        outer.addLayout(top)

        self.custom_date = QDateEdit()
        self.custom_date.setCalendarPopup(True)
        self.custom_date.setDisplayFormat("yyyy-MM-dd")
        self.custom_date.setFixedHeight(38)
        self.custom_date.setStyleSheet(INPUT_STYLE)
        self.custom_date.setDate(QDate.currentDate())
        self.custom_date.setVisible(False)

        cal = self.custom_date.calendarWidget()
        if cal is not None:
            cal.setStyleSheet(CALENDAR_STYLE)
            cal.setGridVisible(False)

        outer.addWidget(self.custom_date)

        self.when_combo.currentIndexChanged.connect(self._on_when_changed)

        if data:
            self._load(data)

    def _on_when_changed(self):
        when = self.when_combo.currentData()
        self.custom_date.setVisible(when == "custom")

    def _load(self, data):
        if "when" in data:
            when_value = data["when"]
            custom_date_str = data.get("custom_date")
        else:
            offset = data.get("offset_days", 0)
            when_value = {
                0: "on_day",
                1: "1_day_before",
                7: "1_week_before",
            }.get(offset, "on_day")
            custom_date_str = None

        idx = self.when_combo.findData(when_value)
        if idx >= 0:
            self.when_combo.setCurrentIndex(idx)

        if custom_date_str:
            d = QDate.fromString(custom_date_str, "yyyy-MM-dd")
            if d.isValid():
                self.custom_date.setDate(d)

        hh = int(data.get("hour", 9))
        mm = int(data.get("minute", 0))
        hour_12 = hh % 12
        if hour_12 == 0:
            hour_12 = 12
        ampm = "AM" if hh < 12 else "PM"
        self.hour.setValue(hour_12)
        self.minute.setValue(mm)
        self.ampm.setCurrentText(ampm)

        sound = data.get("sound", "Gentle")
        s_idx = self.sound.findText(sound)
        if s_idx >= 0:
            self.sound.setCurrentIndex(s_idx)

        self._on_when_changed()

    def to_dict(self):
        when = self.when_combo.currentData()

        custom = None
        if when == "custom":
            custom = self.custom_date.date().toString("yyyy-MM-dd")

        h = self.hour.value()
        if self.ampm.currentText() == "AM":
            h24 = 0 if h == 12 else h
        else:
            h24 = 12 if h == 12 else h + 12

        return {
            "when": when,
            "custom_date": custom,
            "hour": h24,
            "minute": self.minute.value(),
            "sound": self.sound.currentText(),
        }


class RemindersDialog(QDialog):
    """Clean, balanced reminder editor used from the Add Event dialog."""

    FIXED_WIDTH = 700
    MAX_HEIGHT = 680

    def __init__(self, reminders=None, parent=None):
        super().__init__(parent)
        self._rows = []

        self.setWindowTitle("Add Reminders")
        self.setModal(True)
        self.setMinimumWidth(self.FIXED_WIDTH)
        self.setMaximumHeight(self.MAX_HEIGHT)
        self.setStyleSheet(DIALOG_STYLE)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(LARGE, LARGE, LARGE, LARGE)
        layout.setSpacing(MEDIUM)

        header_row = QHBoxLayout()
        header_row.setContentsMargins(0, 0, 0, 0)
        header_row.setSpacing(SMALL)

        icon = QLabel("🔔")
        icon.setFixedSize(38, 38)
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon.setStyleSheet(
            f"background: rgba(54, 204, 209, 0.10);"
            f" border: 1px solid rgba(54, 204, 209, 0.20);"
            f" border-radius: 11px;"
            f" font-size: 18px;"
        )

        header = QLabel("Reminders")
        header.setStyleSheet(EVENT_DIALOG_HEADER)

        header_row.addWidget(icon)
        header_row.addWidget(header)
        header_row.addStretch()
        layout.addLayout(header_row)

        sub = QLabel(
            "Choose when you want to be reminded about this event. "
            "Each reminder can use a different time and sound."
        )
        sub.setWordWrap(True)
        sub.setStyleSheet(
            f"color: {TEXT_SECONDARY};"
            f" font-family: {FONT_STACK}; font-size: 12px;"
            f" background: transparent;"
        )
        layout.addWidget(sub)

        section = QFrame()
        section.setObjectName("reminderSection")
        section.setStyleSheet(
            f"QFrame#reminderSection {{"
            f" background: rgba(79, 124, 255, 0.035);"
            f" border: 1px solid {BORDER};"
            f" border-radius: 14px;"
            f"}}"
        )
        section_layout = QVBoxLayout(section)
        section_layout.setContentsMargins(MEDIUM, MEDIUM, MEDIUM, MEDIUM)
        section_layout.setSpacing(SMALL)

        section_title = QLabel("Reminder schedule")
        section_title.setStyleSheet(EVENT_FORM_LABEL)
        section_layout.addWidget(section_title)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.scroll.setStyleSheet(
            f"QScrollArea {{ background: transparent; border: none; }}"
            f"QScrollBar:vertical {{"
            f" background: transparent; width: 9px; margin: 2px 0; }}"
            f"QScrollBar::handle:vertical {{"
            f" background: {TEXT_SECONDARY}; border-radius: 4px; min-height: 34px;"
            f" margin: 2px; }}"
            f"QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{"
            f" height: 0; }}"
        )

        self.rows_container = QWidget()
        self.rows_container.setStyleSheet("background: transparent;")
        self.rows_layout = QVBoxLayout(self.rows_container)
        self.rows_layout.setContentsMargins(0, 0, 0, 0)
        self.rows_layout.setSpacing(SMALL)
        self.rows_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll.setWidget(self.rows_container)
        section_layout.addWidget(self.scroll, 1)

        self.empty_label = QLabel("No reminders yet. Add one below.")
        self.empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.empty_label.setStyleSheet(
            f"color: {TEXT_SECONDARY};"
            f" font-family: {FONT_STACK}; font-size: 13px;"
            f" padding: 16px 0; background: transparent;"
        )
        section_layout.addWidget(self.empty_label)

        layout.addWidget(section, 1)

        self.add_btn = QPushButton("+   Add Reminder")
        self.add_btn.setFixedHeight(44)
        self.add_btn.setStyleSheet(EVENT_ADD_REMINDER_BUTTON)
        self.add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.add_btn.clicked.connect(lambda: self._add_row(None))
        layout.addWidget(self.add_btn)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(MEDIUM)
        btn_row.addStretch()

        cancel = QPushButton("Cancel")
        cancel.setFixedSize(110, 42)
        cancel.setStyleSheet(EVENT_CANCEL_BUTTON)
        cancel.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel.clicked.connect(self.reject)

        save = QPushButton("Save")
        save.setFixedSize(110, 42)
        save.setStyleSheet(EVENT_SAVE_BUTTON)
        save.setCursor(Qt.CursorShape.PointingHandCursor)
        save.clicked.connect(self.accept)

        btn_row.addWidget(cancel)
        btn_row.addWidget(save)
        layout.addLayout(btn_row)

        for reminder in (reminders or []):
            self._add_row(reminder)

        self._refresh_empty()
        self._fit_height()

    def _fit_height(self):
        self.adjustSize()
        desired = max(360, min(self.sizeHint().height(), self.MAX_HEIGHT))
        self.resize(self.FIXED_WIDTH, desired)

    def _add_row(self, data):
        row = ReminderRow(on_remove=self._remove_row, data=data)
        self._rows.append(row)
        self.rows_layout.addWidget(row)
        self._refresh_empty()
        self._fit_height()

    def _remove_row(self, row):
        if row not in self._rows:
            return
        self._rows.remove(row)
        self.rows_layout.removeWidget(row)
        row.deleteLater()
        self._refresh_empty()
        self._fit_height()

    def _refresh_empty(self):
        self.empty_label.setVisible(len(self._rows) == 0)

    def value(self):
        return [row.to_dict() for row in self._rows]
