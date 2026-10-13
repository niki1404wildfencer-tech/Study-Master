from PySide6.QtCore import Qt, Signal

from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QSpinBox )

from ui.styles.styles import COMBO_BOX, selector_label_style


class DurationSelector(QWidget):

    duration_changed = Signal(int)

    def __init__(self):
        super().__init__()

        self.setup_ui()
        self.connect_signals()

    def setup_ui(self):
        layout = QVBoxLayout()

        layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        layout.setSpacing(5)

        self.title = QLabel(
            "Duration"
        )

        self.title.setAlignment(
            Qt.AlignmentFlag.AlignLeft
        )

        self.title.setStyleSheet(
            selector_label_style
        )

        self.spin = QSpinBox()

        self.spin.setStyleSheet(
            COMBO_BOX
        )

        self.spin.setMinimum(1)
        self.spin.setMaximum(300)
        self.spin.setValue(20)
        self.spin.setSuffix(" min")

        self.spin.setMinimumHeight(
            42
        )

        layout.addWidget(
            self.title
        )

        layout.addWidget(
            self.spin
        )

        self.setLayout(
            layout
        )
    def connect_signals(self):
        self.spin.valueChanged.connect(self.duration_changed.emit)

    def current_duration(self):
        return self.spin.value()
    def get_duration_seconds(self):
        return self.spin.value() * 60


