from datetime import datetime
import jdatetime

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout

from ui.styles.styles import time_label_style
from ui.styles.fonts import FONT_FAMILY, CLOCK_SIZE, SUBTITLE_SIZE


class ClockWidget(QWidget):

    def __init__(self, clock_size=None, date_size=None, parent=None):
        super().__init__(parent)
        self.clock_size = clock_size if clock_size is not None else CLOCK_SIZE
        self.date_size = date_size if date_size is not None else SUBTITLE_SIZE

        self.setup_ui()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        self.update_time()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(4)

        clock_font = QFont(FONT_FAMILY, self.clock_size, QFont.Weight.Bold)
        date_font = QFont(FONT_FAMILY, self.date_size, QFont.Weight.DemiBold)

        # تاریخ میلادی
        self.date_Label = QLabel()
        self.date_Label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.date_Label.setFont(date_font)
        self.date_Label.setStyleSheet(time_label_style)

        # ساعت
        self.Time_Label = QLabel()
        self.Time_Label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.Time_Label.setFont(clock_font)
        self.Time_Label.setStyleSheet(time_label_style)

        # تاریخ شمسی
        self.shamsi_Label = QLabel()
        self.shamsi_Label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.shamsi_Label.setFont(date_font)
        self.shamsi_Label.setStyleSheet(time_label_style)

        layout.addWidget(self.date_Label)
        layout.addWidget(self.Time_Label)
        layout.addWidget(self.shamsi_Label)
        self.setLayout(layout)

    def update_time(self):
        now = datetime.now()
        self.Time_Label.setText(now.strftime("%H : %M : %S"))
        self.date_Label.setText(now.strftime("%A , %d / %B / %Y"))
        shamsi = jdatetime.datetime.now()
        self.shamsi_Label.setText(shamsi.strftime(" %Y / %m / %d"))