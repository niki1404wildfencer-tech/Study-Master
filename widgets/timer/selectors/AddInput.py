from PySide6.QtWidgets import (
    QDialog,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QColorDialog,
)
from PySide6.QtCore import Qt

from ui.styles.styles import DIALOG_STYLE
from ui.styles.spacing import MEDIUM, LARGE


class AddInput(QDialog):

    def __init__(
        self,
        title,
        placeholder,
        parent=None,
        name="",
        color="#36CCD1",
    ):

        super().__init__(parent)

        self.selected_color = color

        self.setWindowTitle(title)
        self.setModal(True)

        self.resize(520, 340)
        self.setMinimumSize(480, 300)

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
            LARGE,
        )

        layout.setSpacing(
            MEDIUM
        )

        self.name_label = QLabel(
            "Subject name"
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

        self.color_label = QLabel(
            "Subject color"
        )

        self.color_button = QPushButton(
            "Choose color"
        )

        self.color_button.setMinimumHeight(
            48
        )

        self.update_color_button()

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

        layout.addWidget(
            self.color_label
        )

        layout.addWidget(
            self.color_button
        )

        layout.addStretch()

        layout.addLayout(
            button_row
        )

    def connect_signals(self):

        self.color_button.clicked.connect(
            self.choose_color
        )

        self.save_button.clicked.connect(
            self.accept
        )

        self.cancel_button.clicked.connect(
            self.reject
        )

    def choose_color(self):

        color = QColorDialog.getColor(
            parent=self,
            title="Choose Subject Color",
        )

        if not color.isValid():
            return

        self.selected_color = color.name()

        self.update_color_button()

    def update_color_button(self):

        self.color_button.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {self.selected_color};
                color: white;
                border: none;
                border-radius: 12px;
                padding: 10px;
                font-size: 16px;
                font-weight: 600;
            }}

            QPushButton:hover {{
                opacity: 0.9;
            }}
            """
        )

    def value(self):

        return (
            self.name_input.text().strip(),
            self.selected_color,
        )