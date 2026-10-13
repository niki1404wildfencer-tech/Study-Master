from PySide6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.ticker import FuncFormatter
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
import jdatetime


class StudyTrendChart(QWidget):

    def __init__(self):
        super().__init__()
        self.figure = Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.canvas)

    # ─────────────────────────────────────────
    @staticmethod
    def _gregorian_fmt(x, pos):
        try:
            date = mdates.num2date(x).date()
            return date.strftime("%m/%d")
        except Exception:
            return ""

    @staticmethod
    def _shamsi_fmt(x, pos):
        try:
            date = mdates.num2date(x).date()
            jdate = jdatetime.date.fromgregorian(date=date)
            return jdate.strftime("%m/%d")
        except Exception:
            return ""

    # ─────────────────────────────────────────
    def plot(self, data, color_map=None, subject_map=None,
             period="Weekly", calendar_type="gregorian"):

        self.figure.clear()
        axes = self.figure.add_subplot(111)

        # ─── اگه داده نیست ───
        if data is None or data.empty:
            axes.text(0.5, 0.5, "No study data yet",
                      ha="center", va="center",
                      transform=axes.transAxes, fontsize=14)
            axes.set_xticks([])
            axes.set_yticks([])
            for sp in axes.spines.values():
                sp.set_visible(False)
            self.figure.tight_layout()
            self.canvas.draw()
            return

        # ─── آمادهسازی ───
        data = data.copy()
        data["date"] = pd.to_datetime(data["date"])
        data["subject_id"] = data["subject_id"].fillna(-1).astype(int)

        # ─── pivot: dates × subjects ───
        pivot = data.pivot_table(
            index="date",
            columns="subject_id",
            values="actual_duration",
            aggfunc="sum",
            fill_value=0,
        )

        # ─── تعیین بازه کامل ───
        today = pd.Timestamp.today().normalize()

        if period == "Weekly":
            full_dates = pd.date_range(
                today - pd.Timedelta(days=6), today, freq="D"
            )
        elif period == "Monthly":
            full_dates = pd.date_range(
                today.replace(day=1), today, freq="D"
            )
        elif period == "Yearly":
            full_dates = pd.date_range(
                (today - pd.Timedelta(days=364)).replace(day=1),
                today,
                freq="MS",   # Month Start
            )
        else:  # All Time
            # از اولین ماه داده تا امروز
            first_date = pivot.index.min()
            full_dates = pd.date_range(
                first_date.replace(day=1),
                today,
                freq="MS",
            )

        # ─── reindex ───
        pivot = pivot.reindex(full_dates, fill_value=0)

        # ─── stack کردن ───
        bottom = np.zeros(len(full_dates))

        # ─── اطمینان از ترتیب ثابت ───
        subject_ids = sorted([c for c in pivot.columns])

        for sid in subject_ids:
            values = pivot[sid].values
            color = (color_map or {}).get(sid, "#94A3B8")
            label = (subject_map or {}).get(
                sid,
                "No Subject" if sid == -1 else f"ID {sid}",
            )
            axes.bar(
                full_dates,
                values,
                bottom=bottom,
                color=color,
                label=label,
                width=0.7,
            )
            bottom += values

        # ─── فرمت محور X ───
        fmt = self._shamsi_fmt if calendar_type == "shamsi" else self._gregorian_fmt
        axes.xaxis.set_major_formatter(FuncFormatter(fmt))
        axes.xaxis.set_major_locator(mdates.AutoDateLocator())

        axes.set_ylabel("Minutes")
        axes.set_title("Study Trend")
        axes.tick_params(axis="x", rotation=45, labelsize=9)
        axes.tick_params(axis="y", labelsize=9)

        if len(subject_ids) > 0:
            axes.legend(
                loc="upper right",
                fontsize=8,
                framealpha=0.9,
            )

        self.figure.tight_layout()
        self.canvas.draw()