from datetime import datetime, date
import calendar as py_calendar

import jdatetime

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QSizePolicy, QFrame
)
from PySide6.QtCore import Qt, Signal

from managers.CalendarManager import get_calendar_manager
from ui.styles.spacing import SMALL, MEDIUM
from ui.styles.styles import (
    selector_shared,
    CALENDAR_TITLE, CALENDAR_DAY_NAME,
    CALENDAR_DAY_CELL, CALENDAR_DAY_CELL_TODAY, CALENDAR_DAY_CELL_WEEKEND,
    CALENDAR_DAY_NUMBER, CALENDAR_DAY_NUMBER_TODAY, CALENDAR_DAY_NUMBER_WEEKEND,
    CALENDAR_DAY_BADGE,
)
from widgets.calendar.EventChip import EventChip

# ─── rokh (Persian view only) ───
try:
    from rokh import get_events, DateSystem
    ROKH_AVAILABLE = True
except ImportError:
    ROKH_AVAILABLE = False

# ─── holidays (English, Gregorian view) ───
try:
    import holidays as holidays_lib
    HOLIDAYS_AVAILABLE = True
except ImportError as exc:
    HOLIDAYS_AVAILABLE = False
    print(
        "[Calendar] holidays could not be imported. "
        "Install it in the same Python environment used to run Study Dash "
        "with: python -m pip install holidays. "
        f"Details: {exc}"
    )


# All of these output English names.
HOLIDAY_COUNTRIES = ["US", "GB", "CA", "AU", "NZ", "IE"]


GREGORIAN_MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]
GREGORIAN_DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
GREGORIAN_WEEKEND = 6

SHAMSI_MONTHS = [
    "فروردین", "اردیبهشت", "خرداد", "تیر",
    "مرداد", "شهریور", "مهر", "آبان",
    "آذر", "دی", "بهمن", "اسفند"
]
SHAMSI_DAYS = [
    "شنبه", "یک‌شنبه", "دوشنبه", "سه‌شنبه",
    "چهارشنبه", "پنج‌شنبه", "جمعه"
]
SHAMSI_WEEKEND = 6


def jalaali_days_in_month(year, month):
    if month <= 6:
        return 31
    if month <= 11:
        return 30
    return 30 if year % 33 in (1, 5, 9, 13, 17, 22, 26, 30) else 29


def _extract_name(raw):
    """The holidays library returns a str or a list of str — normalise."""
    if isinstance(raw, (list, tuple)):
        return str(raw[0]) if raw else ""
    return str(raw) if raw else ""


# Common international / cultural observances shown in English.
# These are complementary to the country holiday data returned by `holidays`.
FIXED_INTERNATIONAL_EVENTS = {
    (1, 1): "New Year's Day",
    (1, 4): "World Braille Day",
    (1, 24): "International Day of Education",
    (1, 27): "International Holocaust Remembrance Day",
    (2, 2): "World Wetlands Day",
    (2, 4): "World Cancer Day",
    (2, 6): "International Day of Zero Tolerance for Female Genital Mutilation",
    (2, 11): "International Day of Women and Girls in Science",
    (2, 13): "World Radio Day",
    (2, 20): "World Day of Social Justice",
    (2, 21): "International Mother Language Day",
    (3, 3): "World Wildlife Day",
    (3, 8): "International Women's Day",
    (3, 20): "International Day of Happiness",
    (3, 21): (
        "International Day for the Elimination of Racial Discrimination",
        "World Poetry Day",
        "International Day of Forests",
    ),
    (3, 22): "World Water Day",
    (3, 23): "World Meteorological Day",
    (3, 24): "World Tuberculosis Day",
    (4, 2): "World Autism Awareness Day",
    (4, 7): "World Health Day",
    (4, 22): "Earth Day",
    (4, 23): "World Book and Copyright Day",
    (4, 25): "World Malaria Day",
    (4, 26): "World Intellectual Property Day",
    (4, 28): "World Day for Safety and Health at Work",
    (5, 3): "World Press Freedom Day",
    (5, 15): "International Day of Families",
    (5, 17): "World Telecommunication and Information Society Day",
    (5, 20): "World Bee Day",
    (5, 22): "International Day for Biological Diversity",
    (5, 29): "International Day of UN Peacekeepers",
    (5, 31): "World No Tobacco Day",
    (6, 3): "World Bicycle Day",
    (6, 5): "World Environment Day",
    (6, 8): "World Oceans Day",
    (6, 12): "World Day Against Child Labour",
    (6, 14): "World Blood Donor Day",
    (6, 17): "World Day to Combat Desertification and Drought",
    (6, 20): "World Refugee Day",
    (6, 21): "International Day of Yoga",
    (6, 23): "United Nations Public Service Day",
    (6, 26): "International Day Against Drug Abuse and Illicit Trafficking",
    (6, 30): "International Asteroid Day",
    (7, 11): "World Population Day",
    (7, 15): "World Youth Skills Day",
    (7, 18): "Nelson Mandela International Day",
    (7, 30): "International Day of Friendship",
    (8, 9): "International Day of the World's Indigenous Peoples",
    (8, 12): "International Youth Day",
    (8, 19): "World Humanitarian Day",
    (8, 23): "International Day for the Remembrance of the Slave Trade and its Abolition",
    (8, 30): "International Day of the Victims of Enforced Disappearances",
    (9, 8): "International Literacy Day",
    (9, 15): "International Day of Democracy",
    (9, 16): "International Day for the Preservation of the Ozone Layer",
    (9, 21): "International Day of Peace",
    (9, 27): "World Tourism Day",
    (9, 28): "International Day for Universal Access to Information",
    (9, 30): "International Translation Day",
    (10, 1): "International Day of Older Persons",
    (10, 2): "International Day of Non-Violence",
    (10, 5): "World Teachers' Day",
    (10, 10): "World Mental Health Day",
    (10, 11): "International Day of the Girl Child",
    (10, 16): "World Food Day",
    (10, 17): "International Day for the Eradication of Poverty",
    (10, 24): (
        "United Nations Day",
        "World Development Information Day",
    ),
    (10, 31): "Halloween",
    (11, 5): "World Tsunami Awareness Day",
    (11, 10): "World Science Day for Peace and Development",
    (11, 14): "World Diabetes Day",
    (11, 16): "International Day for Tolerance",
    (11, 19): "World Toilet Day",
    (11, 20): "World Children's Day",
    (11, 25): "International Day for the Elimination of Violence against Women",
    (12, 1): "World AIDS Day",
    (12, 3): "International Day of Persons with Disabilities",
    (12, 5): "International Volunteer Day",
    (12, 9): "International Anti-Corruption Day",
    (12, 10): "Human Rights Day",
    (12, 18): "International Migrants Day",
    (12, 20): "International Human Solidarity Day",
    (12, 24): "Christmas Eve",
    (12, 25): "Christmas Day",
    (12, 26): "Boxing Day",
    (12, 31): "New Year's Eve",
}


def get_gregorian_holidays(year):
    """Return English Gregorian holidays/observances as date -> list metadata."""
    combined = {}

    def add_event(day, title, is_holiday=False):
        if not day or not title:
            return
        combined.setdefault(day, [])
        # Avoid duplicate labels when two providers return the same event.
        if not any(item["title"] == title for item in combined[day]):
            combined[day].append({
                "title": title,
                "is_holiday": bool(is_holiday),
            })

    # Country-specific public holidays and observances.
    if HOLIDAYS_AVAILABLE:
        for country in HOLIDAY_COUNTRIES:
            try:
                h = holidays_lib.country_holidays(country, years=year)
                for d, raw in h.items():
                    add_event(d, _extract_name(raw), True)
            except Exception as exc:
                print(f"[Calendar] public holidays for {country} failed: {exc}")

            try:
                h = holidays_lib.country_holidays(
                    country, years=year, categories="observance"
                )
                for d, raw in h.items():
                    add_event(d, _extract_name(raw), False)
            except Exception:
                pass

    # Common fixed international/cultural observances.
    for (month, day), titles in FIXED_INTERNATIONAL_EVENTS.items():
        if isinstance(titles, (list, tuple)):
            for title in titles:
                add_event(date(year, month, day), title, False)
        else:
            add_event(date(year, month, day), titles, False)

    # One event can have more than one label.  Keep them all; the renderer can
    # show the first badge and include every event in the day tooltip.
    return combined


# ═══════════════════════════════════════════
# DayCell
# ═══════════════════════════════════════════
class DayCell(QFrame):

    clicked = Signal(object)
    event_clicked = Signal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.date_str = None
        self.events = []
        self.is_today = False
        self.is_weekend = False
        self.is_holiday = False

        self.setFixedHeight(84)
        self.setCursor(Qt.CursorShape.ArrowCursor)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(2)

        self.day_label = QLabel()
        self.day_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop
        )
        layout.addWidget(self.day_label)

        self.badge_label = QLabel()
        self.badge_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.badge_label.setStyleSheet(CALENDAR_DAY_BADGE)
        self.badge_label.hide()
        layout.addWidget(self.badge_label)

        self.chips_container = QWidget()
        self.chips_container.setStyleSheet("background: transparent;")
        self.chips_layout = QVBoxLayout(self.chips_container)
        self.chips_layout.setContentsMargins(0, 0, 0, 0)
        self.chips_layout.setSpacing(2)
        self.chips_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.chips_container, 1)

        self._reset()

    def _reset(self):
        self.date_str = None
        self.events = []
        self.is_today = False
        self.is_weekend = False
        self.is_holiday = False
        self.day_label.setText("")
        self.badge_label.setText("")
        self.badge_label.hide()
        self.setStyleSheet(CALENDAR_DAY_CELL)
        self.setCursor(Qt.CursorShape.ArrowCursor)
        self.setToolTip("")
        self._clear_chips()

    def _clear_chips(self):
        while self.chips_layout.count():
            item = self.chips_layout.takeAt(0)
            w = item.widget()
            if w is not None:
                w.deleteLater()

    def set_day(self, day, date_str, is_today, is_weekend, events):
        self.date_str = date_str
        self.events = events
        self.is_today = is_today
        self.is_weekend = is_weekend
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self.day_label.setText(str(day))

        holiday_events = [e for e in events if e.get("is_holiday")]
        personal_events = [e for e in events if e.get("is_personal", False)]
        self.is_holiday = len(holiday_events) > 0

        if is_today:
            self.setStyleSheet(CALENDAR_DAY_CELL_TODAY)
            self.day_label.setStyleSheet(CALENDAR_DAY_NUMBER_TODAY)
        elif is_weekend or self.is_holiday:
            self.setStyleSheet(CALENDAR_DAY_CELL_WEEKEND)
            self.day_label.setStyleSheet(CALENDAR_DAY_NUMBER_WEEKEND)
        else:
            self.setStyleSheet(CALENDAR_DAY_CELL)
            self.day_label.setStyleSheet(CALENDAR_DAY_NUMBER)

        if holiday_events:
            t = holiday_events[0].get("title", "")
            if len(t) > 16:
                t = t[:15] + "…"
            self.badge_label.setText(t)
            self.badge_label.show()
        else:
            self.badge_label.hide()

        self._clear_chips()
        max_chips = 2
        for ev in personal_events[:max_chips]:
            chip = EventChip(ev, self)
            chip.clicked.connect(self.event_clicked.emit)
            self.chips_layout.addWidget(chip)

        if len(personal_events) > max_chips:
            more = QLabel(f"+{len(personal_events) - max_chips} more")
            more.setStyleSheet(
                'background: transparent; color: #ffffff;'
                'font-family: "Segoe UI", "Vazirmatn"; font-size: 9px; font-weight: 600;'
            )
            self.chips_layout.addWidget(more)

        # Tooltip: every event on the day, red dot for real holidays.
        tooltip_lines = []
        for e in events:
            mark = "🔴 " if e.get("is_holiday") else "• "
            tooltip_lines.append(f"{mark}{e.get('title', '')}")
        self.setToolTip("\n".join(tooltip_lines))

    def mousePressEvent(self, event):
        if self.date_str is not None:
            self.clicked.emit(self)
        super().mousePressEvent(event)


# ═══════════════════════════════════════════
# CalendarWidget
# ═══════════════════════════════════════════
class CalendarWidget(QWidget):

    day_clicked = Signal(str, list)
    event_clicked = Signal(dict)

    def __init__(self, calendar_type="gregorian", parent=None):
        super().__init__(parent)

        self.calendar_type = calendar_type
        self._year = None
        self._month = None
        self._day_cells = []
        self._day_name_labels = []
        self._events_cache = {}
        self._gregorian_holidays_cache = {}

        self.calendar_manager = get_calendar_manager()
        self.calendar_manager.event_changed.connect(self._render)

        self.setup_ui()
        self.connect_signals()
        self._go_to_today()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(MEDIUM)

        header = QHBoxLayout()
        header.setSpacing(SMALL)

        self.prev_btn = QPushButton("‹")
        self.prev_btn.setFixedSize(44, 44)
        self.prev_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.prev_btn.setStyleSheet(selector_shared)

        self.next_btn = QPushButton("›")
        self.next_btn.setFixedSize(44, 44)
        self.next_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.next_btn.setStyleSheet(selector_shared)

        self.title_label = QLabel()
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet(CALENDAR_TITLE)

        self.today_btn = QPushButton("Today")
        self.today_btn.setFixedHeight(44)
        self.today_btn.setMinimumWidth(90)
        self.today_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.today_btn.setStyleSheet(selector_shared)

        header.addWidget(self.prev_btn)
        header.addStretch()
        header.addWidget(self.title_label, 3)
        header.addStretch()
        header.addWidget(self.today_btn)
        header.addWidget(self.next_btn)
        main_layout.addLayout(header)

        names_layout = QHBoxLayout()
        names_layout.setSpacing(4)
        for _ in range(7):
            lbl = QLabel()
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setStyleSheet(CALENDAR_DAY_NAME)
            self._day_name_labels.append(lbl)
            names_layout.addWidget(lbl)
        main_layout.addLayout(names_layout)

        self.days_grid = QGridLayout()
        self.days_grid.setSpacing(4)

        for row in range(6):
            for col in range(7):
                cell = DayCell()
                cell.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
                cell.clicked.connect(self._on_day_clicked)
                cell.event_clicked.connect(self.event_clicked.emit)
                self.days_grid.addWidget(cell, row, col)
                self._day_cells.append(cell)

        main_layout.addLayout(self.days_grid)

    def connect_signals(self):
        self.prev_btn.clicked.connect(self._go_prev)
        self.next_btn.clicked.connect(self._go_next)
        self.today_btn.clicked.connect(self._go_to_today)

    def _go_prev(self):
        self._month -= 1
        if self._month < 1:
            self._month = 12
            self._year -= 1
        self._render()

    def _go_next(self):
        self._month += 1
        if self._month > 12:
            self._month = 1
            self._year += 1
        self._render()

    def _go_to_today(self):
        if self.calendar_type == "gregorian":
            now = datetime.now()
            self._year = now.year
            self._month = now.month
        else:
            now = jdatetime.date.today()
            self._year = now.year
            self._month = now.month
        self._render()

    def set_calendar_type(self, cal_type):
        if cal_type not in ("gregorian", "shamsi"):
            return
        if cal_type == self.calendar_type:
            return
        self.calendar_type = cal_type
        self._go_to_today()

    def _render(self):
        for cell in self._day_cells:
            cell._reset()

        if self.calendar_type == "gregorian":
            self._render_gregorian()
        else:
            self._render_shamsi()

    # ═══════════════════════════════════════════
    # GREGORIAN
    # ═══════════════════════════════════════════
    def _render_gregorian(self):
        year, month = self._year, self._month
        self.title_label.setText(f"{GREGORIAN_MONTHS[month - 1]} {year}")

        for i, name in enumerate(GREGORIAN_DAYS):
            self._day_name_labels[i].setText(name)

        weeks = py_calendar.monthcalendar(year, month)
        today = datetime.now().date()
        holidays_map = self._get_gregorian_holidays(year)

        for week_idx, week in enumerate(weeks):
            if week_idx >= 6:
                break
            for day_idx, day in enumerate(week):
                if day == 0:
                    continue

                cell = self._day_cells[week_idx * 7 + day_idx]
                date_str = f"{year:04d}-{month:02d}-{day:02d}"
                date_obj = date(year, month, day)

                is_today = (
                    year == today.year and
                    month == today.month and
                    day == today.day
                )
                is_weekend = (day_idx == GREGORIAN_WEEKEND)

                all_events = []

                # ── Holidays & observances (English) ──
                for info in holidays_map.get(date_obj, []):
                    all_events.append({
                        "title": info["title"],
                        "color": "#EF4444" if info["is_holiday"] else "#4F7CFF",
                        "is_holiday": info["is_holiday"],
                        "is_personal": False,
                        "is_rokh": False,
                    })

                # ── Personal events ──
                for e in self.calendar_manager.get_events_for_date(date_str):
                    ev = e.copy()
                    ev["is_holiday"] = False
                    ev["is_personal"] = True
                    ev["is_rokh"] = False
                    all_events.append(ev)

                cell.set_day(day, date_str, is_today, is_weekend, all_events)

    # ═══════════════════════════════════════════
    # SHAMSI — unchanged
    # ═══════════════════════════════════════════
    def _render_shamsi(self):
        year, month = self._year, self._month
        self.title_label.setText(f"{SHAMSI_MONTHS[month - 1]} {year}")

        for i, name in enumerate(SHAMSI_DAYS):
            self._day_name_labels[i].setText(name)

        first_day = jdatetime.date(year, month, 1)
        first_weekday = first_day.weekday()
        days_in_month = jalaali_days_in_month(year, month)
        today = jdatetime.date.today()
        rokh_events_map = self._get_events_for_month(year, month, "shamsi")

        day = 1
        for week_idx in range(6):
            for day_idx in range(7):
                if week_idx == 0 and day_idx < first_weekday:
                    continue
                if day > days_in_month:
                    continue

                cell = self._day_cells[week_idx * 7 + day_idx]

                try:
                    g = jdatetime.date(year, month, day).togregorian()
                    date_str = f"{g.year:04d}-{g.month:02d}-{g.day:02d}"
                except Exception:
                    date_str = None

                is_today = (
                    year == today.year and
                    month == today.month and
                    day == today.day
                )
                is_weekend = (day_idx == SHAMSI_WEEKEND)

                all_events = []

                for e in rokh_events_map.get(day, []):
                    all_events.append({
                        "title": e.get("description", ""),
                        "color": "#EF4444",
                        "is_holiday": bool(e.get("is_holiday", False)),
                        "is_personal": False,
                        "is_rokh": True,
                    })

                if date_str:
                    for e in self.calendar_manager.get_events_for_date(date_str):
                        ev = e.copy()
                        ev["is_holiday"] = False
                        ev["is_personal"] = True
                        ev["is_rokh"] = False
                        all_events.append(ev)

                cell.set_day(day, date_str, is_today, is_weekend, all_events)
                day += 1

    def _on_day_clicked(self, cell):
        self.day_clicked.emit(cell.date_str, cell.events)

    # ═══════════════════════════════════════════
    # Rokh — SHAMSI view only
    # ═══════════════════════════════════════════
    def _get_events_for_month(self, year, month, cal_type):
        cache_key = (year, month, cal_type)
        if cache_key in self._events_cache:
            return self._events_cache[cache_key]

        result = {}
        if not ROKH_AVAILABLE:
            self._events_cache[cache_key] = result
            return result

        if cal_type == "gregorian":
            days_in_month = py_calendar.monthrange(year, month)[1]
            date_system = DateSystem.GREGORIAN
            wanted_keys = ["gregorian"]
        else:
            days_in_month = jalaali_days_in_month(year, month)
            date_system = DateSystem.JALALI
            wanted_keys = ["jalali", "hijri"]

        for day in range(1, days_in_month + 1):
            try:
                events_data = get_events(
                    day=day, month=month, year=year,
                    input_date_system=date_system,
                )
            except Exception:
                continue

            day_events = []
            events_dict = events_data.get("events", {})

            for key in wanted_keys:
                for e in events_dict.get(key, []):
                    day_events.append({
                        "description": e.get("description", ""),
                        "is_holiday": e.get("is_holiday", False),
                        "source": key,
                    })

            if day_events:
                result[day] = day_events

        self._events_cache[cache_key] = result
        return result

    def _get_gregorian_holidays(self, year):
        if year in self._gregorian_holidays_cache:
            return self._gregorian_holidays_cache[year]
        result = get_gregorian_holidays(year)
        self._gregorian_holidays_cache[year] = result
        return result