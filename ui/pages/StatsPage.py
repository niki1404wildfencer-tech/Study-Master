from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QSizePolicy, QFileDialog, QMenu,
)
from PySide6.QtCore import Qt, QSize, QPoint
from PySide6.QtGui import QIcon

from widgets.stats.StudyTrendChart import StudyTrendChart
from widgets.stats.SubjectTimeChart import SubjectTimeChart

from managers.StatsManager import StatisticsManager
from managers.SessionManager import get_session_manager
from managers.SubjectManager import SubjectManager
from managers.SettingsManager import SettingsManager

from ui.components.card import Card
from ui.styles.spacing import *
from ui.styles.styles import menu_label_style, selector, button_style , selector_shared

from assets.icon.icon import CALENDAR_ICON


class StatsPage(QWidget):

    def __init__(self):
        super().__init__()

        self.session_manager = get_session_manager()
        self.subject_manager = SubjectManager()
        self.settings_manager = SettingsManager()
        self.statistics_manager = StatisticsManager()

        self.calendar_type = "gregorian"

        self.setup_ui()
        self.connect_signals()
        self.refresh()

    # =========================================================
    # UI
    # =========================================================
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(LARGE, LARGE, LARGE, LARGE)
        layout.setSpacing(MEDIUM)

        # ─── Title ───
        self.title = QLabel("Statistics")
        self.title.setStyleSheet(menu_label_style)
        layout.addWidget(self.title)

        # ─── کنترلهای بالا ───
        controls_row = QHBoxLayout()
        controls_row.setSpacing(SMALL)

        self.period_sel = QComboBox()
        self.period_sel.addItems(
            ["Weekly", "Monthly", "Yearly", "All Time"]
        )
        self.period_sel.setStyleSheet(selector_shared)
        self.period_sel.setFixedSize(160, 46)

        # ─── دکمه تقویم (کنار سلکتور) ───
        self.calendar_btn = QPushButton()
        self.calendar_btn.setIcon(QIcon(str(CALENDAR_ICON)))
        self.calendar_btn.setIconSize(QSize(22, 22))
        self.calendar_btn.setFixedSize(46, 46)
        self.calendar_btn.setStyleSheet(selector_shared)
        self.calendar_btn.setToolTip("Calendar type")
        self.calendar_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        # ساخت منو (بدون setMenu، با کلیک باز میشه)
        self.calendar_menu = QMenu(self)
        self.calendar_menu.setStyleSheet("""
            QMenu {
                background-color: #FFFFFF;
                border: 1px solid #E4E8F0;
                border-radius: 10px;
                padding: 6px;
                font-family: "Segoe UI";
                font-size: 14px;
            }
            QMenu::item {
                padding: 8px 24px;
                border-radius: 6px;
            }
            QMenu::item:selected {
                background-color: rgba(79, 124, 255, 0.12);
                color: #4F7CFF;
            }
        """)
        self.calendar_menu.addAction(
            "Gregorian",
            lambda: self.set_calendar("gregorian"),
        )
        self.calendar_menu.addAction(
            "Shamsi (Persian)",
            lambda: self.set_calendar("shamsi"),
        )

        controls_row.addWidget(self.period_sel)
        controls_row.addWidget(self.calendar_btn)
        controls_row.addStretch()
        layout.addLayout(controls_row)

        # ─── Summary cards ───
        summary_row = QHBoxLayout()
        summary_row.setSpacing(MEDIUM)

        self.goal_card, self.goal_value = self._make_stat_card(
            "Daily Goal", "0m / 0m"
        )
        self.subject_card, self.most_studied_value = self._make_stat_card(
            "Most Studied", "No Data"
        )
        self.average_card, self.average_session_value = self._make_stat_card(
            "Average Session", "0 min"
        )

        summary_row.addWidget(self.goal_card, 1)
        summary_row.addWidget(self.subject_card, 1)
        summary_row.addWidget(self.average_card, 1)
        layout.addLayout(summary_row)

        # ─── Charts ───
        chart_row = QHBoxLayout()
        chart_row.setSpacing(MEDIUM)

        self.trend_card = Card()
        self.trend_card.setMinimumHeight(0)
        self.trend_title = QLabel("Daily Study Trend")
        self.trend_chart = StudyTrendChart()
        self.trend_chart.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )
        self.trend_card.add_widget(self.trend_title)
        self.trend_card.add_widget(self.trend_chart)

        self.subject_card_chart = Card()
        self.subject_card_chart.setMinimumHeight(0)
        self.subject_chart_title = QLabel("Study Time By Subject")
        self.subject_chart = SubjectTimeChart()
        self.subject_chart.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )
        self.subject_card_chart.add_widget(self.subject_chart_title)
        self.subject_card_chart.add_widget(self.subject_chart)

        chart_row.addWidget(self.trend_card, 1)
        chart_row.addWidget(self.subject_card_chart, 1)
        layout.addLayout(chart_row, 1)

        # ─── Export ───
        button_row = QHBoxLayout()
        button_row.addStretch()
        self.export_btn = QPushButton("Export PDF")
        self.export_btn.setStyleSheet(button_style)
        button_row.addWidget(self.export_btn)
        layout.addLayout(button_row)

        self.setLayout(layout)

    # =========================================================
    def _make_stat_card(self, title_text, value_text):
        card = Card()
        card.setMinimumHeight(0)
        card.setMaximumHeight(140)

        title = QLabel(title_text)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                color: #6B7280;
                background: transparent;
                font-family: "Segoe UI";
                font-size: 15px;
                font-weight: 600;
            }
        """)

        value = QLabel(value_text)
        value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        value.setStyleSheet("""
            QLabel {
                color: #1F2937;
                background: transparent;
                font-family: "Segoe UI";
                font-size: 26px;
                font-weight: 800;
            }
        """)

        card.add_widget(title)
        card.add_widget(value)
        return card, value

    # =========================================================
    def connect_signals(self):
        self.period_sel.currentTextChanged.connect(self.period_changed)
        self.export_btn.clicked.connect(self.export_pdf)
        self.calendar_btn.clicked.connect(self._show_calendar_menu)

        self.session_manager.session_completed.connect(
            lambda _: self.refresh()
        )

    def _show_calendar_menu(self):
        # منو رو زیر دکمه باز کن
        pos = self.calendar_btn.mapToGlobal(
            QPoint(0, self.calendar_btn.height())
        )
        self.calendar_menu.exec(pos)

    # =========================================================
    def showEvent(self, event):
        super().showEvent(event)
        self.refresh()

    # =========================================================
    def refresh(self):
        self.statistics_manager.set_sessions(
            self.session_manager.get_sessions()
        )
        self.statistics_manager.set_daily_goal(
            self.settings_manager.get_daily_goal_minutes()
        )
        self.update_statistics()

    # =========================================================
    def update_statistics(self):
        goal_data = self.statistics_manager.get_daily_goal_data()
        goal = goal_data["goal_minutes"]
        studied = goal_data["studied_minutes"]
        self.goal_value.setText(
            f"{self._format_minutes(studied)} / "
            f"{self._format_minutes(goal)}"
        )

        average = self.statistics_manager.get_average_session_duration()
        self.average_session_value.setText(f"{average:.0f} min")

        most_studied_id = self.statistics_manager.get_most_studied_subject()
        if most_studied_id is not None:
            subject = self.subject_manager.get_subject(most_studied_id)
            name = subject["name"] if subject else f"ID {most_studied_id}"
            self.most_studied_value.setText(name)
        else:
            self.most_studied_value.setText("No Data")

        self.update_trend_chart()
        self.update_subject_chart()

    def _format_minutes(self, minutes):
        minutes = int(minutes)
        if minutes < 60:
            return f"{minutes}m"
        return f"{minutes / 60:.1f}h"

    # =========================================================
    def period_changed(self, period):
        self.update_trend_chart()

    def set_calendar(self, cal_type):
        self.calendar_type = cal_type
        self.update_trend_chart()

    # =========================================================
    def update_trend_chart(self):
        period = self.period_sel.currentText()
        data = self.statistics_manager.get_daily_trend_by_subject(period)

        color_map = {}
        subject_map = {}
        for subject in self.subject_manager.get_subjects():
            color_map[subject["id"]] = subject["color"]
            subject_map[subject["id"]] = subject["name"]

        self.trend_chart.plot(
            data,
            color_map,
            subject_map,
            period,
            self.calendar_type,
        )

    def update_subject_chart(self):
        data = self.statistics_manager.get_study_time_by_subject_df()
        self.subject_chart.plot(data, self.subject_manager)

    # =========================================================
    def export_pdf(self):
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Statistics as PDF",
            "statistics.pdf",
            "PDF Files (*.pdf)",
        )
        if not path:
            return
        if not path.lower().endswith(".pdf"):
            path += ".pdf"

        try:
            from matplotlib.backends.backend_pdf import PdfPages
            with PdfPages(path) as pdf:
                pdf.savefig(self.trend_chart.figure)
                pdf.savefig(self.subject_chart.figure)
            print(f"PDF saved to: {path}")
        except Exception as e:
            print(f"Export failed: {e}")