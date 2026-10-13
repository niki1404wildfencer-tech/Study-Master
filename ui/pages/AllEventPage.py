from datetime import datetime, timedelta

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QFrame, QComboBox
)
from PySide6.QtCore import Qt, Signal

from managers.CalendarManager import get_calendar_manager
from managers.SubjectManager import SubjectManager

from ui.styles.styles import (
    menu_label_style, selector_shared, EVENT_SCROLL_AREA,
)
from ui.styles.spacing import LARGE, MEDIUM, SMALL


FILTERS = [
    ("Today", "today"),
    ("This Week", "week"),
    ("This Month", "month"),
    ("All", "all"),
    ("Past", "past"),
]


class EventRow(QFrame):
    clicked = Signal(dict)

    def __init__(self, event, subject_name="", parent=None):
        super().__init__(parent)
        self._event_data = event
        self._hovered = False

        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedHeight(78)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(MEDIUM, SMALL, MEDIUM, SMALL)
        layout.setSpacing(MEDIUM)

        bar = QFrame()
        bar.setFixedWidth(6)
        bar.setStyleSheet(
            f"background: {event.get('color', '#4F7CFF')}; border-radius: 3px;"
        )
        layout.addWidget(bar)

        date_col = QVBoxLayout()
        date_col.setSpacing(2)

        date_str = event.get("date", "")
        try:
            d = datetime.strptime(date_str, "%Y-%m-%d").date()
            day_text, weekday_text = d.strftime("%d %b"), d.strftime("%A")
        except Exception:
            day_text, weekday_text = date_str, ""

        day_lbl = QLabel(day_text)
        day_lbl.setFixedWidth(70)
        day_lbl.setStyleSheet(
            'background: transparent; color: #1F2937;'
            'font-family: "Segoe UI", "Vazirmatn"; font-size: 18px; font-weight: 800;'
        )
        wd_lbl = QLabel(weekday_text)
        wd_lbl.setFixedWidth(70)
        wd_lbl.setStyleSheet(
            'background: transparent; color: #6B7280;'
            'font-family: "Segoe UI", "Vazirmatn"; font-size: 11px;'
        )
        date_col.addWidget(day_lbl)
        date_col.addWidget(wd_lbl)

        text_col = QVBoxLayout()
        text_col.setSpacing(2)

        title_lbl = QLabel(event.get("title", "(untitled)"))
        title_lbl.setStyleSheet(
            'background: transparent; color: #1F2937;'
            'font-family: "Segoe UI", "Vazirmatn"; font-size: 16px; font-weight: 700;'
        )

        meta = []
        if event.get("time"):
            meta.append(event["time"])
        if subject_name:
            meta.append(subject_name)
        details = event.get("details", "")
        if details:
            meta.append(details[:40] + ("…" if len(details) > 40 else ""))
        meta_lbl = QLabel("  •  ".join(meta))
        meta_lbl.setStyleSheet(
            'background: transparent; color: #6B7280;'
            'font-family: "Segoe UI", "Vazirmatn"; font-size: 12px;'
        )

        text_col.addWidget(title_lbl)
        text_col.addWidget(meta_lbl)

        layout.addLayout(date_col)
        layout.addLayout(text_col, 1)

        self._apply_style(False)

    def _apply_style(self, hovered):
        bg = "rgba(79, 124, 255, 0.06)" if hovered else "#FFFFFF"
        border = "#4F7CFF" if hovered else "#E4E8F0"
        self.setStyleSheet(
            f"QFrame {{ background: {bg}; border: 1px solid {border};"
            f" border-radius: 14px; }}"
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


class AllEventsPage(QWidget):

    event_selected = Signal(dict)
    back_requested = Signal()

    def __init__(self):
        super().__init__()
        self.calendar_manager = get_calendar_manager()
        self.subject_manager = SubjectManager()
        self.current_filter = "week"

        self.setup_ui()
        self.connect_signals()

        self.calendar_manager.event_changed.connect(self.refresh)
        self.subject_manager.subject_changed.connect(self.refresh)
        self.refresh()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(LARGE, LARGE, LARGE, LARGE)
        layout.setSpacing(MEDIUM)

        header_row = QHBoxLayout()
        header_row.setSpacing(MEDIUM)

        self.back_btn = QPushButton("← Back")
        self.back_btn.setStyleSheet(selector_shared)
        self.back_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.back_btn.setFixedHeight(44)
        header_row.addWidget(self.back_btn)

        title = QLabel("All My Events")
        title.setStyleSheet(menu_label_style)
        header_row.addWidget(title)
        header_row.addStretch()

        self.filter_sel = QComboBox()
        for label, value in FILTERS:
            self.filter_sel.addItem(label, value)
        self.filter_sel.setCurrentIndex(1)
        self.filter_sel.setFixedSize(180, 46)
        self.filter_sel.setStyleSheet(selector_shared)
        header_row.addWidget(self.filter_sel)

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

        self.empty_label = QLabel("No events to show.")
        self.empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.empty_label.setStyleSheet(
            'color: #6B7280; font-family: "Segoe UI", "Vazirmatn";'
            'font-size: 15px; background: transparent;'
        )
        layout.addWidget(self.empty_label)

    def connect_signals(self):
        self.back_btn.clicked.connect(self.back_requested.emit)
        self.filter_sel.currentIndexChanged.connect(self._on_filter_changed)

    def _on_filter_changed(self):
        self.current_filter = self.filter_sel.currentData()
        self.refresh()

    def _subject_lookup(self):
        return {s["id"]: s["name"] for s in self.subject_manager.get_subjects()}

    def _filter_events(self, events):
        today = datetime.now().date()
        if self.current_filter == "all":
            return events

        filtered = []
        for e in events:
            try:
                d = datetime.strptime(e.get("date", ""), "%Y-%m-%d").date()
            except Exception:
                continue

            if self.current_filter == "today" and d == today:
                filtered.append(e)
            elif self.current_filter == "week":
                start = today - timedelta(days=today.weekday())
                if start <= d <= start + timedelta(days=6):
                    filtered.append(e)
            elif self.current_filter == "month":
                if d.year == today.year and d.month == today.month:
                    filtered.append(e)
            elif self.current_filter == "past" and d < today:
                filtered.append(e)
        return filtered

    def _clear_list(self):
        while self.list_layout.count():
            item = self.list_layout.takeAt(0)
            w = item.widget()
            if w is not None:
                w.deleteLater()

    def refresh(self):
        self._clear_list()
        all_events = self.calendar_manager.get_all_events_sorted(
            ascending=(self.current_filter != "past")
        )
        filtered = self._filter_events(all_events)

        if not filtered:
            self.empty_label.setVisible(True)
            return
        self.empty_label.setVisible(False)

        names = self._subject_lookup()
        for ev in filtered:
            row = EventRow(ev, subject_name=names.get(ev.get("subject_id"), ""))
            row.clicked.connect(self.event_selected.emit)
            self.list_layout.addWidget(row)