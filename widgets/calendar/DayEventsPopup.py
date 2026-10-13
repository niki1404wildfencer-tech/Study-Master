from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QFrame, QWidget
)
from PySide6.QtCore import Qt, Signal, QTimer

from ui.styles.styles import (
    DIALOG_STYLE, CALENDAR_TITLE,
    EVENT_SAVE_BUTTON, EVENT_CANCEL_BUTTON, EVENT_SCROLL_AREA,
)
from ui.styles.spacing import LARGE, MEDIUM, SMALL

import jdatetime


class EventListItem(QFrame):
    clicked = Signal(dict)

    def __init__(self, event, parent=None):
        super().__init__(parent)
        self._event_data = event
        self._hovered = False

        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedHeight(66)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(SMALL, SMALL, SMALL, SMALL)
        layout.setSpacing(MEDIUM)

        self.dot = QLabel()
        self.dot.setFixedSize(14, 14)
        self.dot.setStyleSheet(
            f"background: {event.get('color', '#4F7CFF')}; border-radius: 7px;"
        )

        text_col = QVBoxLayout()
        text_col.setSpacing(2)

        title_label = QLabel(event.get("title", "(untitled)"))
        title_label.setStyleSheet(
            'background: transparent; color: #1F2937;'
            'font-family: "Segoe UI", "Vazirmatn"; font-size: 15px; font-weight: 700;'
        )

        time_str = event.get("time", "")
        details = event.get("details", "")
        sub = time_str
        if details:
            sub = f"{time_str}  •  {details}" if time_str else details
        sub_label = QLabel(sub)
        sub_label.setStyleSheet(
            'background: transparent; color: #6B7280;'
            'font-family: "Segoe UI", "Vazirmatn"; font-size: 12px;'
        )

        text_col.addWidget(title_label)
        text_col.addWidget(sub_label)

        layout.addWidget(self.dot, alignment=Qt.AlignmentFlag.AlignTop)
        layout.addLayout(text_col, 1)

        self._apply_style(False)

    def _apply_style(self, hovered):
        bg = "rgba(79, 124, 255, 0.08)" if hovered else "#FFFFFF"
        border = "#4F7CFF" if hovered else "#E4E8F0"
        self.setStyleSheet(
            f"QFrame {{ background: {bg}; border: 1px solid {border};"
            f" border-radius: 12px; }}"
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
        super().mousePressEvent(event)


class DayEventsPopup(QDialog):
    """List of personal events for a clicked day."""

    edit_requested = Signal(dict)
    add_requested = Signal(str)

    def __init__(self, date_str, events, calendar_type="gregorian", parent=None):
        super().__init__(parent)
        self.date_str = date_str
        self.events = events
        self.calendar_type = calendar_type

        self.setWindowTitle("Events")
        self.setModal(True)
        self.resize(520, 560)
        self.setMinimumSize(460, 420)
        self.setStyleSheet(DIALOG_STYLE)

        self._build_ui()
        self._populate()

    def _formatted_date(self):
        try:
            from datetime import datetime
            d = datetime.strptime(self.date_str, "%Y-%m-%d").date()
            if self.calendar_type == "shamsi":
                return jdatetime.date.fromgregorian(date=d).strftime("%Y/%m/%d")
            return d.strftime("%A, %d %B %Y")
        except Exception:
            return self.date_str or ""

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(LARGE, LARGE, LARGE, LARGE)
        layout.setSpacing(MEDIUM)

        header_row = QHBoxLayout()
        header_row.setSpacing(MEDIUM)

        title = QLabel(self._formatted_date())
        title.setStyleSheet(CALENDAR_TITLE)
        header_row.addWidget(title, 1)

        self.add_btn = QPushButton("+ Add")
        self.add_btn.setStyleSheet(EVENT_SAVE_BUTTON)
        self.add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        header_row.addWidget(self.add_btn)
        layout.addLayout(header_row)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet(EVENT_SCROLL_AREA)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.list_container = QWidget()
        self.list_layout = QVBoxLayout(self.list_container)
        self.list_layout.setContentsMargins(0, 0, 0, 0)
        self.list_layout.setSpacing(SMALL)
        self.list_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll.setWidget(self.list_container)
        layout.addWidget(self.scroll, 1)

        self.empty_label = QLabel("No events for this day.")
        self.empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.empty_label.setStyleSheet(
            'color: #6B7280; font-family: "Segoe UI", "Vazirmatn";'
            'font-size: 14px; background: transparent;'
        )
        self.empty_label.hide()
        layout.addWidget(self.empty_label)

        close_row = QHBoxLayout()
        close_row.addStretch()
        close_btn = QPushButton("Close")
        close_btn.setStyleSheet(EVENT_CANCEL_BUTTON)
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.clicked.connect(self.reject)
        close_row.addWidget(close_btn)
        layout.addLayout(close_row)

        self.add_btn.clicked.connect(self._on_add)

    def _on_add(self):
        self.accept()
        QTimer.singleShot(0, lambda: self.add_requested.emit(self.date_str))

    def _populate(self):
        personal = [e for e in self.events if e.get("is_personal", False)]
        personal.sort(key=lambda e: e.get("time", ""))

        if not personal:
            self.empty_label.setVisible(True)
            return

        for ev in personal:
            item = EventListItem(ev)
            item.clicked.connect(self._on_event_clicked)
            self.list_layout.addWidget(item)

    def _on_event_clicked(self, event):
        from managers.CalendarManager import get_calendar_manager
        full = get_calendar_manager().get_event(event.get("id")) or event
        self.accept()
        QTimer.singleShot(0, lambda: self.edit_requested.emit(full))