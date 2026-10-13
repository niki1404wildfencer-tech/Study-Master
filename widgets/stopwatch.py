from PySide6.QtCore import Qt, QTimer , QSize
from PySide6.QtGui import QFont , QIcon
from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout
)
from assets.icon.icon import PLAY_ICON , PAUSE_ICON , RESET_ICON 
from ui.styles.styles import button_style, time_label_style
from ui.styles.fonts import FONT_FAMILY, TIMER_SIZE


class Stopwatch(QWidget):
    """
    Shared-state stopwatch.

    All Stopwatch widgets in the app (dashboard + stopwatch page)
    share the same elapsed time because the state lives on the
    CLASS, not on each instance.
    """

    # ── Shared state (class-level) ──
    _shared_elapsed = 0
    _shared_running = False
    _shared_timer = None
    _instances = []

    def __init__(self, font_size=None, parent=None):
        super().__init__(parent)

        self.font_size = font_size if font_size is not None else TIMER_SIZE

        # Register this widget so ticks reach it
        Stopwatch._instances.append(self)

        # Create the shared timer once, on first Stopwatch ever built
        if Stopwatch._shared_timer is None:
            Stopwatch._shared_timer = QTimer()
            Stopwatch._shared_timer.setInterval(1000)
            Stopwatch._shared_timer.timeout.connect(Stopwatch._tick_all)

        self.setup_ui()

        # Show whatever the shared state is right now
        self._sync_display()

    # =====================================================
    # UI
    # =====================================================

    def setup_ui(self):
        layout = QVBoxLayout()

        time_font = QFont(FONT_FAMILY, self.font_size, QFont.Weight.Bold)

        self.time_label = QLabel("00:00:00")
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.time_label.setFont(time_font)
        self.time_label.setStyleSheet(time_label_style)

        btn_row = QHBoxLayout()
        self.start_btn = QPushButton("start")
        self.pause_btn = QPushButton("pause")
        self.restart_btn = QPushButton("restart")


        self.start_btn.setIcon(QIcon(str(PLAY_ICON)))
        self.start_btn.setIconSize(QSize(22, 22))

        
        self.pause_btn.setIcon(QIcon(str(PAUSE_ICON)))
        self.pause_btn.setIconSize(QSize(22, 22))
        
        self.restart_btn.setIcon(QIcon(str(RESET_ICON)))
        self.restart_btn.setIconSize(QSize(22, 22))
        


        for b in (self.start_btn, self.pause_btn, self.restart_btn):
            b.setStyleSheet(button_style)
            b.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_row.addWidget(b)

        self.start_btn.clicked.connect(self.start_stopwatch)
        self.pause_btn.clicked.connect(self.pause_stopwatch)
        self.restart_btn.clicked.connect(self.restart_stopwatch)

        layout.addWidget(self.time_label)
        layout.addLayout(btn_row)
        self.setLayout(layout)

    # =====================================================
    # Shared timer — called once per second
    # =====================================================

    @classmethod
    def _tick_all(cls):
        cls._shared_elapsed += 1
        # Snapshot first — some widgets may have been destroyed
        for inst in list(cls._instances):
            inst._sync_display()

    # =====================================================
    # Display
    # =====================================================

    def _sync_display(self):
        h = Stopwatch._shared_elapsed // 3600
        m = (Stopwatch._shared_elapsed % 3600) // 60
        s = Stopwatch._shared_elapsed % 60
        try:
            self.time_label.setText(f"{h:02}:{m:02}:{s:02}")
        except RuntimeError:
            # Widget was deleted — drop it from the registry
            try:
                Stopwatch._instances.remove(self)
            except ValueError:
                pass

    # =====================================================
    # Controls
    # =====================================================

    def start_stopwatch(self):
        if Stopwatch._shared_running:
            return
        Stopwatch._shared_running = True
        Stopwatch._shared_timer.start()

    def pause_stopwatch(self):
        Stopwatch._shared_running = False
        Stopwatch._shared_timer.stop()

    def restart_stopwatch(self):
        Stopwatch._shared_timer.stop()
        Stopwatch._shared_running = False
        Stopwatch._shared_elapsed = 0
        for inst in list(Stopwatch._instances):
            inst._sync_display()