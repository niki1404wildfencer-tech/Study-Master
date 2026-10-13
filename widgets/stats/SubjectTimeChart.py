from PySide6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class SubjectTimeChart(QWidget):

    def __init__(self):
        super().__init__()
        self.figure = Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.canvas)

    def plot(self, data_df, subject_manager):
        """
        data_df: DataFrame with columns [subject_id, actual_duration]
        subject_manager: SubjectManager instance
        """
        self.figure.clear()
        axes = self.figure.add_subplot(111)

        # ─── اگه داده خالیه ───
        if data_df is None or data_df.empty:
            axes.text(
                0.5, 0.5, "No data yet",
                ha="center", va="center",
                transform=axes.transAxes, fontsize=14,
            )
            axes.set_xticks([])
            axes.set_yticks([])
            for spine in axes.spines.values():
                spine.set_visible(False)
            self.figure.tight_layout()
            self.canvas.draw()
            return

        labels, sizes, colors = [], [], []

        for _, row in data_df.iterrows():

            subject_id = row["subject_id"]
            minutes = row["actual_duration"]

            if minutes <= 0:
                continue

            subject = subject_manager.get_subject(subject_id)

            name = subject["name"] if subject else f"ID {subject_id}"
            color = subject["color"] if subject else "#94A3B8"

            labels.append(name)
            sizes.append(minutes)
            colors.append(color)

        # ─── اگه هیچ subject معتبری نبود ───
        if not sizes:
            axes.text(
                0.5, 0.5, "No data yet",
                ha="center", va="center",
                transform=axes.transAxes, fontsize=14,
            )
            self.figure.tight_layout()
            self.canvas.draw()
            return

        # ─── pie chart ───
        axes.pie(
            sizes,
            labels=labels,
            colors=colors,
            autopct="%1.0f%%",
            startangle=90,
            textprops={"fontsize": 10},
        )

        axes.axis("equal")
        axes.set_title("Study Time By Subject")

        self.figure.tight_layout()
        self.canvas.draw()