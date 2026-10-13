from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton
)
from PySide6.QtCore import Qt, Signal, QDate
import jdatetime

from ui.styles.styles import SHAMSI_CALENDAR

SHAMSI_MONTHS = [
    "فروردین", "اردیبهشت", "خرداد", "تیر",
    "مرداد", "شهریور", "مهر", "آبان",
    "آذر", "دی", "بهمن", "اسفند"
]

SHAMSI_DAYS_SHORT = ["ش", "ی", "د", "س", "چ", "پ", "ج"]


def _jalaali_days_in_month(year, month):
    if month <= 6:
        return 31
    if month <= 11:
        return 30
    return 30 if year % 33 in (1, 5, 9, 13, 17, 22, 26, 30) else 29


class ShamsiPopupCalendar(QWidget):
    """
    مینی‌کلندر شمسی به‌صورت Popup.
    وقتی کاربر روزی رو انتخاب می‌کنه، QDate میلادی emit می‌شه.
    """

    date_selected = Signal(QDate)

    def __init__(self, initial_qdate=None, parent=None):
        super().__init__(parent)

        # رفتار Popup
        self.setWindowFlags(
            Qt.WindowType.Popup |
            Qt.WindowType.FramelessWindowHint
        )
        self.setAttribute(
            Qt.WidgetAttribute.WA_StyledBackground, True
        )
        self.setStyleSheet(SHAMSI_CALENDAR)

        # تاریخ شروع
        if initial_qdate is not None and initial_qdate.isValid():
            try:
                gd = initial_qdate.toPython()
                self._selected = jdatetime.date.fromgregorian(date=gd)
            except Exception:
                self._selected = jdatetime.date.today()
        else:
            self._selected = jdatetime.date.today()

        self._view_year = self._selected.year
        self._view_month = self._selected.month

        self.setFixedSize(300, 330)

        self._build_ui()
        self._rebuild_grid()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(6)

        # ─── Header ───
        header = QHBoxLayout()
        header.setSpacing(4)

        prev_btn = QPushButton("‹")
        prev_btn.setFixedSize(30, 30)
        prev_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        prev_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                font-size: 18px;
                font-weight: 700;
                color: #4F7CFF;
                border-radius: 8px;
            }
            QPushButton:hover {
                background: rgba(79, 124, 255, 0.10);
            }
        """)
        prev_btn.clicked.connect(self._go_prev)

        next_btn = QPushButton("›")
        next_btn.setFixedSize(30, 30)
        next_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        next_btn.setStyleSheet(prev_btn.styleSheet())
        next_btn.clicked.connect(self._go_next)

        self.header_label = QLabel()
        self.header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.header_label.setStyleSheet("""
            font-family: "Vazirmatn";
            font-size: 15px;
            font-weight: 800;
            color: #1F2937;
            background: transparent;
        """)

        header.addWidget(prev_btn)
        header.addWidget(self.header_label, 1)
        header.addWidget(next_btn)
        layout.addLayout(header)

        # ─── روزهای هفته ───
        names_row = QHBoxLayout()
        names_row.setSpacing(0)

        for name in SHAMSI_DAYS_SHORT:
            lbl = QLabel(name)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setStyleSheet("""
                font-family: "Vazirmatn";
                font-size: 11px;
                font-weight: 700;
                color: #6B7280;
                background: transparent;
            """)
            names_row.addWidget(lbl, 1)

        layout.addLayout(names_row)

        # ─── گرید روزها ───
        self.grid = QGridLayout()
        self.grid.setSpacing(2)
        layout.addLayout(self.grid)

        layout.addStretch()

    def _rebuild_grid(self):
        # پاک کردن
        while self.grid.count():
            item = self.grid.takeAt(0)
            w = item.widget()
            if w is not None:
                w.deleteLater()

        self.header_label.setText(
            f"{SHAMSI_MONTHS[self._view_month - 1]} {self._view_year}"
        )

        first_day = jdatetime.date(
            self._view_year, self._view_month, 1
        )
        first_weekday = first_day.weekday()
        days_in_month = _jalaali_days_in_month(
            self._view_year, self._view_month
        )

        try:
            today = jdatetime.date.today()
        except Exception:
            today = None

        day = 1
        for week_idx in range(6):
            for day_idx in range(7):
                if week_idx == 0 and day_idx < first_weekday:
                    continue
                if day > days_in_month:
                    continue

                btn = QPushButton(str(day))
                btn.setFixedSize(34, 34)
                btn.setCursor(Qt.CursorShape.PointingHandCursor)

                is_today = (
                    today is not None and
                    self._view_year == today.year and
                    self._view_month == today.month and
                    day == today.day
                )
                is_selected = (
                    self._view_year == self._selected.year and
                    self._view_month == self._selected.month and
                    day == self._selected.day
                )

                if is_selected:
                    btn.setStyleSheet("""
                        QPushButton {
                            background: #4F7CFF;
                            color: white;
                            border: none;
                            border-radius: 17px;
                            font-family: "Vazirmatn";
                            font-size: 12px;
                            font-weight: 700;
                        }
                    """)
                elif is_today:
                    btn.setStyleSheet("""
                        QPushButton {
                            background: rgba(79, 124, 255, 0.15);
                            color: #4F7CFF;
                            border: none;
                            border-radius: 17px;
                            font-family: "Vazirmatn";
                            font-size: 12px;
                            font-weight: 700;
                        }
                    """)
                else:
                    btn.setStyleSheet("""
                        QPushButton {
                            background: transparent;
                            color: #1F2937;
                            border: none;
                            border-radius: 17px;
                            font-family: "Vazirmatn";
                            font-size: 12px;
                        }
                        QPushButton:hover {
                            background: rgba(79, 124, 255, 0.10);
                        }
                    """)

                btn.clicked.connect(
                    lambda checked=False, d=day: self._select_day(d)
                )

                self.grid.addWidget(btn, week_idx, day_idx)
                day += 1

    def _go_prev(self):
        self._view_month -= 1
        if self._view_month < 1:
            self._view_month = 12
            self._view_year -= 1
        self._rebuild_grid()

    def _go_next(self):
        self._view_month += 1
        if self._view_month > 12:
            self._view_month = 1
            self._view_year += 1
        self._rebuild_grid()

    def _select_day(self, day):
        jd = jdatetime.date(self._view_year, self._view_month, day)
        gd = jd.togregorian()
        self.date_selected.emit(QDate(gd.year, gd.month, gd.day))
        self.close()