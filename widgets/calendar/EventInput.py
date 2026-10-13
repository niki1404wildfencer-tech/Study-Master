from datetime import date as date_type
from pathlib import Path

import jdatetime

from PySide6.QtWidgets import (
    QDialog, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout,
    QComboBox, QLineEdit, QTextEdit, QPushButton, QColorDialog,
    QSpinBox, QFrame, QWidget, QScrollArea,
    QStackedWidget, QSizePolicy,
)
from PySide6.QtCore import (
    Qt, QDate, QSize, Signal,
)
from PySide6.QtGui import QColor, QPixmap, QIcon

from ui.styles.styles import (
    DIALOG_STYLE,
    COMBO_BOX,
    EVENT_DIALOG_HEADER,
    EVENT_FORM_LABEL,
    EVENT_COLOR_BUTTON,
    EVENT_SAVE_BUTTON,
    EVENT_CANCEL_BUTTON,
    EVENT_DELETE_BUTTON,
    EVENT_VALIDATION_ERROR,
    EVENT_SCROLL_AREA,
    EVENT_COLLAPSIBLE_BUTTON,
)
from ui.styles.spacing import SMALL, MEDIUM, LARGE
from ui.styles.colors import (
    CARD, BORDER, TEXT, PRIMARY, PRIMARY_HOVER, PRIMARY_PRESSED,
    CARD_HOVER,
)
from ui.styles.fonts import FONT_STACK

from assets.SoundSystem import SoundManager
from widgets.calendar.ShamsiPopupCalendar import ShamsiPopupCalendar
from widgets.calendar.GregorianPopupCalendar import GregorianPopupCalendar
from widgets.calendar.RemindersDialog import RemindersDialog


# ─── Constants ───
REPEAT_OPTIONS = [
    ("Does not repeat", "none"),
    ("Daily", "daily"),
    ("Weekly", "weekly"),
    ("Monthly", "monthly"),
    ("Yearly", "yearly"),
]

SHAMSI_MONTHS = [
    "فروردین", "اردیبهشت", "خرداد", "تیر",
    "مرداد", "شهریور", "مهر", "آبان",
    "آذر", "دی", "بهمن", "اسفند"
]

GREGORIAN_MONTHS_SHORT = [
    "01", "02", "03", "04", "05", "06",
    "07", "08", "09", "10", "11", "12"
]


DATE_POPUP_BTN = f"""
QPushButton {{
    background-color: {PRIMARY};
    color: white;
    border: none;
    border-radius: 10px;
    padding: 6px 14px;
    font-family: {FONT_STACK};
    font-size: 15px;
    font-weight: 700;
    text-align: center;
}}
QPushButton:hover {{
    background-color: {PRIMARY_HOVER};
}}
QPushButton:pressed {{
    background-color: {PRIMARY_PRESSED};
}}
"""


def _jalaali_days_in_month(year, month):
    if month <= 6:
        return 31
    if month <= 11:
        return 30
    return 30 if year % 33 in (1, 5, 9, 13, 17, 22, 26, 30) else 29


# ═══════════════════════════════════════════════════════
# Persian Popup Date Input
# ═══════════════════════════════════════════════════════
class PersianPopupDateInput(QWidget):
    dateChanged = Signal(QDate)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._date = QDate.currentDate()

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.btn = QPushButton()
        self.btn.setFixedHeight(44)
        self.btn.setStyleSheet(DATE_POPUP_BTN)
        self.btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn.clicked.connect(self._open_popup)

        layout.addWidget(self.btn)
        self._update_text()

    def _update_text(self):
        try:
            gd = self._date.toPython()
            jd = jdatetime.date.fromgregorian(date=gd)
            self.btn.setText(f"{jd.year:04d}-{jd.month:02d}-{jd.day:02d}")
        except Exception:
            self.btn.setText("")

    def _open_popup(self):
        popup = ShamsiPopupCalendar(initial_qdate=self._date, parent=None)
        popup.date_selected.connect(self._on_selected)
        pos = self.btn.mapToGlobal(self.btn.rect().bottomLeft())
        popup.move(pos)
        popup.show()

    def _on_selected(self, qdate):
        self._date = qdate
        self._update_text()
        self.dateChanged.emit(qdate)

    def setDate(self, qdate):
        self._date = qdate
        self._update_text()

    def date(self):
        return self._date


# ═══════════════════════════════════════════════════════
# Gregorian Popup Date Input
# ═══════════════════════════════════════════════════════
class GregorianPopupDateInput(QWidget):
    dateChanged = Signal(QDate)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._date = QDate.currentDate()

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.btn = QPushButton()
        self.btn.setFixedHeight(44)
        self.btn.setStyleSheet(DATE_POPUP_BTN)
        self.btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn.clicked.connect(self._open_popup)

        layout.addWidget(self.btn)
        self._update_text()

    def _update_text(self):
        self.btn.setText(self._date.toString("yyyy-MM-dd"))

    def _open_popup(self):
        popup = GregorianPopupCalendar(initial_qdate=self._date, parent=None)
        popup.date_selected.connect(self._on_selected)
        pos = self.btn.mapToGlobal(self.btn.rect().bottomLeft())
        popup.move(pos)
        popup.show()

    def _on_selected(self, qdate):
        self._date = qdate
        self._update_text()
        self.dateChanged.emit(qdate)

    def setDate(self, qdate):
        self._date = qdate
        self._update_text()

    def date(self):
        return self._date


# ═══════════════════════════════════════════════════════
# Gregorian Custom Date Input
# ═══════════════════════════════════════════════════════
class GregorianCustomDateInput(QWidget):
    dateChanged = Signal(QDate)

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(SMALL)

        self.year = QSpinBox()
        self.year.setRange(1900, 2100)
        self.year.setFixedHeight(44)
        self.year.setStyleSheet(COMBO_BOX)

        self.month = QComboBox()
        for m in GREGORIAN_MONTHS_SHORT:
            self.month.addItem(m)
        self.month.setFixedHeight(44)
        self.month.setStyleSheet(COMBO_BOX)

        self.day = QSpinBox()
        self.day.setRange(1, 31)
        self.day.setFixedHeight(44)
        self.day.setStyleSheet(COMBO_BOX)

        layout.addWidget(self.year, 2)
        layout.addWidget(self.month, 2)
        layout.addWidget(self.day, 2)

        today = QDate.currentDate()
        self.year.setValue(today.year())
        self.month.setCurrentIndex(today.month() - 1)
        self.day.setValue(today.day())

        self.year.valueChanged.connect(self._emit)
        self.month.currentIndexChanged.connect(self._emit)
        self.day.valueChanged.connect(self._emit)

    def _emit(self):
        qdate = QDate(
            self.year.value(),
            self.month.currentIndex() + 1,
            self.day.value(),
        )
        if qdate.isValid():
            self.dateChanged.emit(qdate)

    def setDate(self, qdate):
        self.year.blockSignals(True)
        self.month.blockSignals(True)
        self.day.blockSignals(True)
        self.year.setValue(qdate.year())
        self.month.setCurrentIndex(qdate.month() - 1)
        self.day.setValue(qdate.day())
        self.year.blockSignals(False)
        self.month.blockSignals(False)
        self.day.blockSignals(False)

    def date(self):
        return QDate(
            self.year.value(),
            self.month.currentIndex() + 1,
            self.day.value(),
        )


# ═══════════════════════════════════════════════════════
# Persian Custom Date Input
# ═══════════════════════════════════════════════════════
class PersianCustomDateInput(QWidget):
    dateChanged = Signal(QDate)

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(SMALL)

        self.year_spin = QSpinBox()
        self.year_spin.setRange(1300, 1500)
        self.year_spin.setFixedHeight(44)
        self.year_spin.setStyleSheet(COMBO_BOX)

        self.month_combo = QComboBox()
        self.month_combo.setFixedHeight(44)
        self.month_combo.setStyleSheet(COMBO_BOX)
        for m in SHAMSI_MONTHS:
            self.month_combo.addItem(m)

        self.day_spin = QSpinBox()
        self.day_spin.setRange(1, 31)
        self.day_spin.setFixedHeight(44)
        self.day_spin.setStyleSheet(COMBO_BOX)

        layout.addWidget(self.year_spin, 3)
        layout.addWidget(self.month_combo, 4)
        layout.addWidget(self.day_spin, 2)

        self._changing = False

        try:
            today = jdatetime.date.today()
            self.year_spin.setValue(today.year)
            self.month_combo.setCurrentIndex(today.month - 1)
            self.day_spin.setValue(today.day)
        except Exception:
            pass

        self.year_spin.valueChanged.connect(self._on_changed)
        self.month_combo.currentIndexChanged.connect(self._on_changed)
        self.day_spin.valueChanged.connect(self._on_changed)

    def _on_changed(self):
        if self._changing:
            return
        self._changing = True
        try:
            y = self.year_spin.value()
            m = self.month_combo.currentIndex() + 1

            max_day = _jalaali_days_in_month(y, m)
            if self.day_spin.maximum() != max_day:
                self.day_spin.setMaximum(max_day)

            d = self.day_spin.value()
            if d > max_day:
                self.day_spin.setValue(max_day)
                d = max_day

            jd = jdatetime.date(y, m, d)
            gd = jd.togregorian()
            self.dateChanged.emit(QDate(gd.year, gd.month, gd.day))
        except Exception:
            pass
        finally:
            self._changing = False

    def setDate(self, qdate):
        try:
            if isinstance(qdate, QDate):
                gd_date = date_type(qdate.year(), qdate.month(), qdate.day())
            else:
                gd_date = qdate
            jd = jdatetime.date.fromgregorian(date=gd_date)
        except Exception:
            return

        self._changing = True
        try:
            self.year_spin.setValue(jd.year)
            self.month_combo.setCurrentIndex(jd.month - 1)
            max_day = _jalaali_days_in_month(jd.year, jd.month)
            self.day_spin.setMaximum(max_day)
            self.day_spin.setValue(jd.day)
        finally:
            self._changing = False

    def date(self):
        try:
            y = self.year_spin.value()
            m = self.month_combo.currentIndex() + 1
            d = self.day_spin.value()
            jd = jdatetime.date(y, m, d)
            gd = jd.togregorian()
            return QDate(gd.year, gd.month, gd.day)
        except Exception:
            return QDate.currentDate()


# ═══════════════════════════════════════════════════════
# AddEvent Dialog
# ═══════════════════════════════════════════════════════
class AddEvent(QDialog):

    def __init__(
        self,
        title="Add Event",
        date_str="",
        subject_manager=None,
        task_manager=None,
        parent=None,
        existing_event=None,
        calendar_type="gregorian",
    ):
        super().__init__(parent)

        self.date_str = date_str
        self.subject_manager = subject_manager
        self.task_manager = task_manager
        self.existing_event = existing_event
        self.calendar_type = calendar_type
        self.selected_color = "#4F7CFF"
        self._current_qdate = QDate.currentDate()
        self._reminders = []

        if existing_event is not None:
            self.selected_color = existing_event.get("color", "#4F7CFF")

        self.setWindowTitle(title)
        self.setModal(True)
        self.resize(720, 800)
        self.setMinimumSize(640, 640)
        self.setStyleSheet(DIALOG_STYLE)

        self.setup_ui()
        self.load_subjects()

        if existing_event is not None:
            self.load_event()
        else:
            self._set_default_date()

        self.connect_signals()
        self._update_date_stack_page()
        self._update_reminders_btn()

    # ═══════════════════════════════════════════
    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(LARGE, LARGE, LARGE, LARGE)
        main_layout.setSpacing(MEDIUM)

        self.header = QLabel(
            "Edit Event" if self.existing_event else "Add Event"
        )
        self.header.setStyleSheet(EVENT_DIALOG_HEADER)
        main_layout.addWidget(self.header)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet(EVENT_SCROLL_AREA)
        self.scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        self.form_widget = QWidget()
        self.form_layout = QVBoxLayout(self.form_widget)
        self.form_layout.setContentsMargins(2, 2, 2, 2)
        self.form_layout.setSpacing(LARGE)

        self._build_form()
        self.scroll.setWidget(self.form_widget)
        main_layout.addWidget(self.scroll, 1)

        self._build_buttons(main_layout)

    # ─── form ───
    def _build_form(self):
        # ══════════════════════════════════════════
        # ROW 1 — Title (2×)  |  Color (1×)
        # ══════════════════════════════════════════
        row1 = QHBoxLayout()
        row1.setSpacing(MEDIUM)

        # ── Left: Title ──
        title_col = QVBoxLayout()
        title_col.setSpacing(SMALL)

        self.title_label = QLabel("📝  Title *")
        self.title_label.setStyleSheet(EVENT_FORM_LABEL)

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Enter event title...")
        self.title_input.setFixedHeight(44)
        self.title_input.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )

        title_col.addWidget(self.title_label)
        title_col.addWidget(self.title_input)

        title_wrap = QWidget()
        title_wrap.setStyleSheet("background: transparent;")
        title_wrap.setLayout(title_col)

        # ── Right: Color ──
        color_col = QVBoxLayout()
        color_col.setSpacing(SMALL)

        self.color_label = QLabel("🎨  Color")
        self.color_label.setStyleSheet(EVENT_FORM_LABEL)

        self.color_button = QPushButton("Choose Color")
        self.color_button.setFixedHeight(44)
        self.color_button.setStyleSheet(EVENT_COLOR_BUTTON)
        self.color_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.color_button.setIconSize(QSize(20, 20))
        self.color_button.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        self._update_color_button()

        color_col.addWidget(self.color_label)
        color_col.addWidget(self.color_button)

        color_wrap = QWidget()
        color_wrap.setStyleSheet("background: transparent;")
        color_wrap.setLayout(color_col)

        row1.addWidget(title_wrap, 1)
        row1.addWidget(color_wrap, 1)
        self.form_layout.addLayout(row1)

        # ══════════════════════════════════════════
        # ROW 2 — Date (50%)  |  Time (50%)
        # ══════════════════════════════════════════
        row2 = QHBoxLayout()
        row2.setSpacing(MEDIUM)

        # ── DATE column ──
        date_col = QVBoxLayout()
        date_col.setSpacing(SMALL)

        date_top = QWidget()
        date_top.setStyleSheet("background: transparent;")
        date_top.setFixedHeight(36)
        date_top_layout = QHBoxLayout(date_top)
        date_top_layout.setContentsMargins(0, 0, 0, 0)
        date_top_layout.setSpacing(SMALL)

        self.date_label = QLabel("📅  Date *")
        self.date_label.setStyleSheet(EVENT_FORM_LABEL)
        date_top_layout.addWidget(self.date_label)
        date_top_layout.addStretch()

        self.calendar_type_combo = QComboBox()
        self.calendar_type_combo.addItem("Gregorian", "gregorian")
        self.calendar_type_combo.addItem("Persian", "shamsi")
        self.calendar_type_combo.setFixedSize(110, 32)
        self.calendar_type_combo.setStyleSheet(COMBO_BOX)
        self.calendar_type_combo.setCursor(Qt.CursorShape.PointingHandCursor)

        self.date_mode_combo = QComboBox()
        self.date_mode_combo.addItem("Popup", "popup")
        self.date_mode_combo.addItem("Custom", "custom")
        self.date_mode_combo.setFixedSize(110, 32)
        self.date_mode_combo.setStyleSheet(COMBO_BOX)
        self.date_mode_combo.setCursor(Qt.CursorShape.PointingHandCursor)

        date_top_layout.addWidget(self.calendar_type_combo)
        date_top_layout.addWidget(self.date_mode_combo)
        date_col.addWidget(date_top)

        self.date_stack = QStackedWidget()
        self.date_stack.setFixedHeight(44)

        self.date_greg_popup = GregorianPopupDateInput()
        self.date_fa_popup = PersianPopupDateInput()
        self.date_greg_custom = GregorianCustomDateInput()
        self.date_fa_custom = PersianCustomDateInput()

        self.date_stack.addWidget(self.date_greg_popup)   # 0
        self.date_stack.addWidget(self.date_fa_popup)     # 1
        self.date_stack.addWidget(self.date_greg_custom)  # 2
        self.date_stack.addWidget(self.date_fa_custom)    # 3

        date_col.addWidget(self.date_stack)

        # ── TIME column ──
        time_col = QVBoxLayout()
        time_col.setSpacing(SMALL)

        time_top = QWidget()
        time_top.setStyleSheet("background: transparent;")
        time_top.setFixedHeight(36)
        time_top_layout = QHBoxLayout(time_top)
        time_top_layout.setContentsMargins(0, 0, 0, 0)
        time_top_layout.setSpacing(SMALL)

        self.time_label = QLabel("🕐  Time")
        self.time_label.setStyleSheet(EVENT_FORM_LABEL)
        time_top_layout.addWidget(self.time_label)
        time_top_layout.addStretch()

        time_col.addWidget(time_top)

        time_inputs = QWidget()
        time_inputs.setStyleSheet("background: transparent;")
        time_inputs.setFixedHeight(44)
        time_inputs_layout = QHBoxLayout(time_inputs)
        time_inputs_layout.setContentsMargins(0, 0, 0, 0)
        time_inputs_layout.setSpacing(SMALL)

        self.hour_input = QSpinBox()
        self.hour_input.setRange(1, 12)
        self.hour_input.setValue(9)
        self.hour_input.setStyleSheet(COMBO_BOX)

        self.minute_input = QSpinBox()
        self.minute_input.setRange(0, 59)
        self.minute_input.setValue(0)
        self.minute_input.setStyleSheet(COMBO_BOX)

        self.ampm_input = QComboBox()
        self.ampm_input.addItems(["AM", "PM"])
        self.ampm_input.setStyleSheet(COMBO_BOX)

        time_inputs_layout.addWidget(self.hour_input, 1)
        time_inputs_layout.addWidget(self.minute_input, 1)
        time_inputs_layout.addWidget(self.ampm_input, 1)

        time_col.addWidget(time_inputs)

        row2.addLayout(date_col, 1)
        row2.addLayout(time_col, 1)
        self.form_layout.addLayout(row2)

        # ── Details ──
        self.details_label = QLabel("📋  Details (optional)")
        self.details_label.setStyleSheet(EVENT_FORM_LABEL)
        self.form_layout.addWidget(self.details_label)

        self.details_input = QTextEdit()
        self.details_input.setPlaceholderText("Extra notes...")
        self.details_input.setFixedHeight(90)
        self.form_layout.addWidget(self.details_input)

        # ── Subject + Task ──
        row4 = QHBoxLayout()
        row4.setSpacing(MEDIUM)

        s_col = QVBoxLayout()
        s_col.setSpacing(SMALL)
        self.subject_label = QLabel("📚  Subject (optional)")
        self.subject_label.setStyleSheet(EVENT_FORM_LABEL)
        self.subject_combo = QComboBox()
        self.subject_combo.setFixedHeight(44)
        self.subject_combo.setStyleSheet(COMBO_BOX)
        s_col.addWidget(self.subject_label)
        s_col.addWidget(self.subject_combo)

        t_col = QVBoxLayout()
        t_col.setSpacing(SMALL)
        self.task_label = QLabel("🎯  Task (optional)")
        self.task_label.setStyleSheet(EVENT_FORM_LABEL)
        self.task_combo = QComboBox()
        self.task_combo.setFixedHeight(44)
        self.task_combo.setStyleSheet(COMBO_BOX)
        t_col.addWidget(self.task_label)
        t_col.addWidget(self.task_combo)

        row4.addLayout(s_col, 1)
        row4.addLayout(t_col, 1)
        self.form_layout.addLayout(row4)

        # ── Repeat ──
        self.repeat_label = QLabel("🔁  Repeat")
        self.repeat_label.setStyleSheet(EVENT_FORM_LABEL)
        self.form_layout.addWidget(self.repeat_label)

        self.repeat_input = QComboBox()
        self.repeat_input.setFixedHeight(44)
        self.repeat_input.setStyleSheet(COMBO_BOX)
        for label, value in REPEAT_OPTIONS:
            self.repeat_input.addItem(label, value)
        self.form_layout.addWidget(self.repeat_input)

        # ── Add Reminders ──
        self.manage_reminders_btn = QPushButton("🔔  Add Reminders")
        self.manage_reminders_btn.setFixedHeight(50)
        self.manage_reminders_btn.setStyleSheet(EVENT_COLLAPSIBLE_BUTTON)
        self.manage_reminders_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.manage_reminders_btn.clicked.connect(self._open_reminders_dialog)
        self.form_layout.addWidget(self.manage_reminders_btn)

    def _open_reminders_dialog(self):
        dialog = RemindersDialog(self._reminders, parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self._reminders = dialog.value()
            self._update_reminders_btn()

    def _update_reminders_btn(self):
        n = len(self._reminders)
        if n == 0:
            self.manage_reminders_btn.setText("🔔  Add Reminders")
        elif n == 1:
            self.manage_reminders_btn.setText("🔔  Add Reminders  •  1 reminder")
        else:
            self.manage_reminders_btn.setText(
                f"🔔  Add Reminders  •  {n} reminders"
            )

    # ─── buttons row ───
    def _build_buttons(self, main_layout):
        btn_row = QHBoxLayout()
        btn_row.setSpacing(MEDIUM)

        self.delete_btn = QPushButton("Delete")
        self.delete_btn.setStyleSheet(EVENT_DELETE_BUTTON)
        self.delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setStyleSheet(EVENT_CANCEL_BUTTON)
        self.cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        self.save_btn = QPushButton("Save")
        self.save_btn.setStyleSheet(EVENT_SAVE_BUTTON)
        self.save_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        if self.existing_event is None:
            self.delete_btn.setVisible(False)

        btn_row.addWidget(self.delete_btn)
        btn_row.addStretch()
        btn_row.addWidget(self.cancel_btn)
        btn_row.addWidget(self.save_btn)
        main_layout.addLayout(btn_row)

    # ─── date stack ───
    def _update_date_stack_page(self):
        cal_type = self.calendar_type_combo.currentData()
        mode = self.date_mode_combo.currentData()

        if cal_type == "gregorian":
            page = 0 if mode == "popup" else 2
        else:
            page = 1 if mode == "popup" else 3

        current_widget = self.date_stack.currentWidget()
        try:
            qdate = current_widget.date()
            if qdate.isValid():
                self._current_qdate = qdate
        except Exception:
            pass

        self.date_stack.setCurrentIndex(page)

        new_widget = self.date_stack.widget(page)
        new_widget.blockSignals(True)
        new_widget.setDate(self._current_qdate)
        new_widget.blockSignals(False)

    def _on_any_date_changed(self, qdate):
        if not qdate.isValid():
            return
        self._current_qdate = qdate

        sender = self.sender()
        for w in (
            self.date_greg_popup, self.date_fa_popup,
            self.date_greg_custom, self.date_fa_custom,
        ):
            if w is sender:
                continue
            w.blockSignals(True)
            try:
                w.setDate(qdate)
            except Exception:
                pass
            w.blockSignals(False)

    def _current_date_input(self):
        return self.date_stack.currentWidget()

    # ─── signals ───
    def connect_signals(self):
        self.color_button.clicked.connect(self.choose_color)
        self.subject_combo.currentIndexChanged.connect(self.on_subject_changed)
        self.cancel_btn.clicked.connect(self.reject)
        self.save_btn.clicked.connect(self.save_event)
        self.delete_btn.clicked.connect(self._delete_and_close)
        self.title_input.textChanged.connect(self._clear_title_error)

        self.calendar_type_combo.currentIndexChanged.connect(
            self._update_date_stack_page
        )
        self.date_mode_combo.currentIndexChanged.connect(
            self._update_date_stack_page
        )

        self.date_greg_popup.dateChanged.connect(self._on_any_date_changed)
        self.date_fa_popup.dateChanged.connect(self._on_any_date_changed)
        self.date_greg_custom.dateChanged.connect(self._on_any_date_changed)
        self.date_fa_custom.dateChanged.connect(self._on_any_date_changed)

    # ─── color ───
    def choose_color(self):
        color = QColorDialog.getColor(
            QColor(self.selected_color), self, "Choose Event Color",
        )
        if color.isValid():
            self.selected_color = color.name()
            self._update_color_button()

    def _update_color_button(self):
        pixmap = QPixmap(20, 20)
        pixmap.fill(QColor(self.selected_color))
        self.color_button.setIcon(QIcon(pixmap))
        self.color_button.setText("  Choose Color")

    def _clear_title_error(self):
        self.title_input.setStyleSheet("")

    # ─── default date ───
    def _set_default_date(self):
        qdate = QDate.currentDate()
        if self.date_str:
            d = QDate.fromString(self.date_str, "yyyy-MM-dd")
            if d.isValid():
                qdate = d

        self._current_qdate = qdate

        for w in (
            self.date_greg_popup, self.date_fa_popup,
            self.date_greg_custom, self.date_fa_custom,
        ):
            w.blockSignals(True)
            try:
                w.setDate(qdate)
            except Exception:
                pass
            w.blockSignals(False)

        if self.calendar_type == "shamsi":
            idx = self.calendar_type_combo.findData("shamsi")
            if idx >= 0:
                self.calendar_type_combo.blockSignals(True)
                self.calendar_type_combo.setCurrentIndex(idx)
                self.calendar_type_combo.blockSignals(False)

    # ─── subject / task ───
    def load_subjects(self):
        self.subject_combo.clear()
        self.subject_combo.addItem("No Subject", None)
        if self.subject_manager is None:
            return
        for subject in self.subject_manager.get_subjects():
            self.subject_combo.addItem(subject["name"], subject["id"])

    def load_tasks(self, subject_id):
        self.task_combo.clear()
        self.task_combo.addItem("No Task", None)
        if subject_id is None or self.task_manager is None:
            return
        for task in self.task_manager.get_tasks(subject_id):
            self.task_combo.addItem(task["name"], task["id"])

    def on_subject_changed(self):
        self.load_tasks(self.subject_combo.currentData())

    # ─── 12h ↔ 24h ───
    @staticmethod
    def _to_24h(hour_12, minute, ampm):
        if ampm == "AM":
            h = 0 if hour_12 == 12 else hour_12
        else:
            h = 12 if hour_12 == 12 else hour_12 + 12
        return h, minute

    @staticmethod
    def _to_12h(hour_24, minute):
        if hour_24 == 0:
            return 12, minute, "AM"
        if hour_24 < 12:
            return hour_24, minute, "AM"
        if hour_24 == 12:
            return 12, minute, "PM"
        return hour_24 - 12, minute, "PM"

    # ─── load existing ───
    def load_event(self):
        ev = self.existing_event
        self.title_input.setText(ev.get("title", ""))
        self.details_input.setPlainText(ev.get("details", ""))

        date_str = ev.get("date", "")
        if date_str:
            d = QDate.fromString(date_str, "yyyy-MM-dd")
            if d.isValid():
                self._current_qdate = d
                for w in (
                    self.date_greg_popup, self.date_fa_popup,
                    self.date_greg_custom, self.date_fa_custom,
                ):
                    w.blockSignals(True)
                    try:
                        w.setDate(d)
                    except Exception:
                        pass
                    w.blockSignals(False)

        time_str = ev.get("time", "09:00")
        try:
            hh, mm = time_str.split(":")
            hour_12, minute, ampm = self._to_12h(int(hh), int(mm))
            self.hour_input.setValue(hour_12)
            self.minute_input.setValue(minute)
            self.ampm_input.setCurrentText(ampm)
        except Exception:
            pass

        repeat = ev.get("repeat", "none")
        idx = self.repeat_input.findData(repeat)
        if idx >= 0:
            self.repeat_input.setCurrentIndex(idx)

        sid = ev.get("subject_id")
        if sid is not None:
            idx = self.subject_combo.findData(sid)
            if idx >= 0:
                self.subject_combo.setCurrentIndex(idx)

        self.load_tasks(sid)

        tid = ev.get("task_id")
        if tid is not None:
            idx = self.task_combo.findData(tid)
            if idx >= 0:
                self.task_combo.setCurrentIndex(idx)

        self._reminders = list(ev.get("reminders", []) or [])

    # ─── save ───
    def save_event(self):
        title = self.title_input.text().strip()
        if not title:
            self.title_input.setStyleSheet(EVENT_VALIDATION_ERROR)
            self.title_input.setFocus()
            return

        current = self._current_date_input()
        try:
            qdate = current.date()
        except Exception:
            qdate = QDate.currentDate()
        date_str = qdate.toString("yyyy-MM-dd")

        h24, m = self._to_24h(
            self.hour_input.value(),
            self.minute_input.value(),
            self.ampm_input.currentText(),
        )
        time_str = f"{h24:02d}:{m:02d}"

        self._title = title
        self._details = self.details_input.toPlainText().strip()
        self._color = self.selected_color
        self._date = date_str
        self._time = time_str
        self._subject_id = self.subject_combo.currentData()
        self._task_id = self.task_combo.currentData()
        self._repeat = self.repeat_input.currentData() or "none"
        self._reminders = list(self._reminders)

        self.accept()

    def _delete_and_close(self):
        self.done(2)

    def value(self):
        return {
            "title": getattr(self, "_title", ""),
            "details": getattr(self, "_details", ""),
            "color": getattr(self, "_color", "#4F7CFF"),
            "date": getattr(self, "_date", ""),
            "time": getattr(self, "_time", "09:00"),
            "subject_id": getattr(self, "_subject_id", None),
            "task_id": getattr(self, "_task_id", None),
            "repeat": getattr(self, "_repeat", "none"),
            "reminders": getattr(self, "_reminders", []),
        }
    # ═══════════════════════════════════════════════════════
# EventViewer — info dialog with Edit button
# ═══════════════════════════════════════════════════════
class EventViewer(QDialog):
    """
    اطلاعات یک ایونت + دکمه Edit که می‌ره به AddEvent.
    """

    edit_requested = Signal(dict)

    def __init__(self, event, subject=None, task=None, parent=None):
        super().__init__(parent)
        # Do NOT name this attribute `event`: QDialog already has an `event()`
        # method, and shadowing it breaks Qt's event dispatch with: 
        # "'dict' object is not callable".
        self._event = event

        self.setWindowTitle(event.get("title", "Event"))
        self.setModal(True)
        self.setMinimumWidth(560)
        self.resize(600, 520)
        self.setStyleSheet(DIALOG_STYLE)

        accent = event.get("color", PRIMARY)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Header ──
        header = QFrame()
        header.setStyleSheet(
            f"QFrame {{"
            f" background: rgba(79, 124, 255, 0.08);"
            f" border-top-left-radius: 18px;"
            f" border-top-right-radius: 18px;"
            f" border-bottom: 1px solid {BORDER};"
            f"}}"
        )
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(LARGE, LARGE, LARGE, LARGE)
        header_layout.setSpacing(MEDIUM)

        dot = QLabel()
        dot.setFixedSize(14, 14)
        dot.setStyleSheet(f"background: {accent}; border-radius: 7px;")

        title_lbl = QLabel(event.get("title", "(untitled)"))
        title_lbl.setWordWrap(True)
        title_lbl.setStyleSheet(
            f"color: {TEXT};"
            f" font-family: {FONT_STACK};"
            f" font-size: 22px; font-weight: 800;"
            f" background: transparent;"
        )

        header_layout.addWidget(dot, alignment=Qt.AlignmentFlag.AlignTop)
        header_layout.addWidget(title_lbl, 1)
        root.addWidget(header)

        # ── Body ──
        body = QWidget()
        body.setStyleSheet(f"background: {CARD};")
        body_layout = QVBoxLayout(body)
        body_layout.setContentsMargins(LARGE, LARGE, LARGE, MEDIUM)
        body_layout.setSpacing(MEDIUM)

        def info_row(icon, label, value):
            row = QWidget()
            row.setStyleSheet("background: transparent;")
            rl = QHBoxLayout(row)
            rl.setContentsMargins(0, 0, 0, 0)
            rl.setSpacing(SMALL)

            ic = QLabel(icon)
            ic.setFixedWidth(24)
            ic.setStyleSheet("background: transparent; font-size: 15px;")
            ic.setAlignment(Qt.AlignmentFlag.AlignTop)

            col = QVBoxLayout()
            col.setSpacing(2)

            lb = QLabel(label)
            lb.setStyleSheet(
                f"color: #6B7280; font-family: {FONT_STACK};"
                f" font-size: 11px; font-weight: 700;"
                f" background: transparent;"
            )

            vl = QLabel(value)
            vl.setWordWrap(True)
            vl.setStyleSheet(
                f"color: {TEXT}; font-family: {FONT_STACK};"
                f" font-size: 14px; font-weight: 600;"
                f" background: transparent;"
            )

            col.addWidget(lb)
            col.addWidget(vl)

            rl.addWidget(ic)
            rl.addLayout(col, 1)
            body_layout.addWidget(row)

        # Date
        date_str = event.get("date", "")
        if date_str:
            display = date_str
            try:
                from datetime import datetime as _dt
                d = _dt.strptime(date_str, "%Y-%m-%d").date()
                display = d.strftime("%A, %d %B %Y")
            except Exception:
                pass
            info_row("📅", "DATE", display)

        # Time
        time_str = event.get("time", "")
        if time_str:
            display = time_str
            try:
                hh, mm = time_str.split(":")
                h24 = int(hh)
                ampm = "AM" if h24 < 12 else "PM"
                h12 = h24 % 12 or 12
                display = f"{h12}:{mm} {ampm}"
            except Exception:
                pass
            info_row("🕐", "TIME", display)

        # Repeat
        repeat = event.get("repeat", "none")
        if repeat and repeat != "none":
            labels = {
                "daily": "Every day",
                "weekly": "Every week",
                "monthly": "Every month",
                "yearly": "Every year",
            }
            info_row("🔁", "REPEAT", labels.get(repeat, repeat))

        # Subject / Task chips
        if subject or task:
            chips_row = QHBoxLayout()
            chips_row.setSpacing(SMALL)
            chips_row.setContentsMargins(0, 0, 0, 0)

            if subject:
                c = QLabel(f"📚  {subject['name']}")
                col = subject.get("color", PRIMARY)
                c.setStyleSheet(
                    f"QLabel {{"
                    f" background: {col}22;"
                    f" color: {col};"
                    f" border-radius: 9px;"
                    f" padding: 4px 12px;"
                    f" font-family: {FONT_STACK};"
                    f" font-size: 12px; font-weight: 700;"
                    f"}}"
                )
                chips_row.addWidget(c)

            if task:
                c = QLabel(f"🎯  {task['name']}")
                c.setStyleSheet(
                    f"QLabel {{"
                    f" background: #6B728022;"
                    f" color: #6B7280;"
                    f" border-radius: 9px;"
                    f" padding: 4px 12px;"
                    f" font-family: {FONT_STACK};"
                    f" font-size: 12px; font-weight: 700;"
                    f"}}"
                )
                chips_row.addWidget(c)

            chips_row.addStretch()
            chips_wrap = QWidget()
            chips_wrap.setStyleSheet("background: transparent;")
            chips_wrap.setLayout(chips_row)
            body_layout.addWidget(chips_wrap)

        # Details
        details = (event.get("details", "") or "").strip()
        if details:
            dl = QLabel("📋  DETAILS")
            dl.setStyleSheet(
                f"color: #6B7280; font-family: {FONT_STACK};"
                f" font-size: 11px; font-weight: 700;"
                f" background: transparent;"
            )
            body_layout.addWidget(dl)

            dbox = QTextEdit()
            dbox.setReadOnly(True)
            dbox.setPlainText(details)
            dbox.setStyleSheet(
                f"QTextEdit {{"
                f" background: {CARD_HOVER};"
                f" border: 1px solid {BORDER};"
                f" border-radius: 10px;"
                f" padding: 10px;"
                f" color: {TEXT};"
                f" font-family: {FONT_STACK}; font-size: 14px;"
                f"}}"
            )
            dbox.setFixedHeight(90)
            body_layout.addWidget(dbox)

        # Reminders
        reminders = event.get("reminders", []) or []
        if reminders:
            rl = QLabel(f"🔔  {len(reminders)} REMINDER(S)")
            rl.setStyleSheet(
                f"color: #6B7280; font-family: {FONT_STACK};"
                f" font-size: 11px; font-weight: 700;"
                f" background: transparent;"
            )
            body_layout.addWidget(rl)

            for r in reminders:
                when = r.get("when", "")
                when_labels = {
                    "on_day": "On the day",
                    "1_day_before": "1 day before",
                    "1_week_before": "1 week before",
                    "custom": f"Custom — {r.get('custom_date', '')}",
                }
                hh = int(r.get("hour", 9))
                mm = int(r.get("minute", 0))
                ampm = "AM" if hh < 12 else "PM"
                h12 = hh % 12 or 12
                txt = (
                    f"  •  {when_labels.get(when, when)} "
                    f"at {h12}:{mm:02d} {ampm}  —  "
                    f"{r.get('sound', 'None')}"
                )
                line = QLabel(txt)
                line.setStyleSheet(
                    f"color: {TEXT}; font-family: {FONT_STACK};"
                    f" font-size: 13px; background: transparent;"
                    f" padding: 2px 0;"
                )
                body_layout.addWidget(line)

        body_layout.addStretch()
        root.addWidget(body, 1)

        # ── Footer ──
        footer = QFrame()
        footer.setStyleSheet(
            f"QFrame {{"
            f" background: {CARD};"
            f" border-top: 1px solid {BORDER};"
            f" border-bottom-left-radius: 18px;"
            f" border-bottom-right-radius: 18px;"
            f"}}"
        )
        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(LARGE, MEDIUM, LARGE, LARGE)
        footer_layout.setSpacing(MEDIUM)
        footer_layout.addStretch()

        close_btn = QPushButton("Close")
        close_btn.setFixedSize(120, 44)
        close_btn.setStyleSheet(EVENT_CANCEL_BUTTON)
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.clicked.connect(self.reject)

        edit_btn = QPushButton("  Edit")
        edit_btn.setFixedSize(120, 44)
        edit_btn.setStyleSheet(EVENT_SAVE_BUTTON)
        edit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        edit_btn.clicked.connect(self._on_edit)

        footer_layout.addWidget(close_btn)
        footer_layout.addWidget(edit_btn)
        root.addWidget(footer)

    def _on_edit(self):
        ev = self._event
        self.accept()
        self.edit_requested.emit(ev)