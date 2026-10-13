from PySide6.QtWidgets import (
    QDialog,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
)
from PySide6.QtCore import Qt

from ui.styles.styles import DIALOG_STYLE
from ui.styles.spacing import MEDIUM, LARGE


class TaskInput(QDialog):

    def __init__(
        self,
        title,
        placeholder,
        parent=None,
        name="",
    ):

        super().__init__(parent)

        self.setWindowTitle(
            title
        )

        self.setModal(True)

        self.resize(
            520,
            280
        )

        self.setMinimumSize(
            480,
            250
        )

        self.setStyleSheet(
            DIALOG_STYLE
        )

        self.setup_ui(
            placeholder,
            name
        )

        self.connect_signals()

    def setup_ui(
        self,
        placeholder,
        name,
    ):

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            LARGE,
            LARGE,
            LARGE,
            LARGE
        )

        layout.setSpacing(
            MEDIUM
        )

        self.name_label = QLabel(
            "Task name"
        )

        self.name_input = QLineEdit()

        self.name_input.setPlaceholderText(
            placeholder
        )

        self.name_input.setText(
            name
        )

        self.name_input.setMinimumHeight(
            48
        )

        button_row = QHBoxLayout()

        button_row.addStretch()

        self.cancel_button = QPushButton(
            "Cancel"
        )

        self.cancel_button.setObjectName(
            "cancelButton"
        )

        self.save_button = QPushButton(
            "Save"
        )

        button_row.addWidget(
            self.cancel_button
        )

        button_row.addWidget(
            self.save_button
        )

        layout.addWidget(
            self.name_label
        )

        layout.addWidget(
            self.name_input
        )

        layout.addStretch()

        layout.addLayout(
            button_row
        )

    def connect_signals(self):

        self.save_button.clicked.connect(
            self.accept
        )

        self.cancel_button.clicked.connect(
            self.reject
        )

    def value(self):

        return self.name_input.text().strip()