from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QStyle, QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor, QFont

from ui.styles.styles import (
    MESSAGE_BOX_DIALOG,
    MESSAGE_BOX_TITLE,
    MESSAGE_BOX_TEXT,
    MESSAGE_BOX_PRIMARY_BTN,
    MESSAGE_BOX_DANGER_BTN,
    MESSAGE_BOX_CANCEL_BTN,
)
from ui.components.CelebrationAnimation import CelebrationAnimation
from assets.SoundSystem import SoundManager


# استایل دکمه سبز جشن (kept from original)
SUCCESS_BUTTON_STYLE = """
QPushButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #34D399, stop:1 #10B981);
    color: white;
    border: none;
    border-radius: 14px;
    padding: 14px 40px;
    font-family: "Segoe UI";
    font-size: 17px;
    font-weight: 700;
    letter-spacing: 0.5px;
}
QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #4ADE80, stop:1 #22C55E);
}
QPushButton:pressed {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #10B981, stop:1 #059669);
    padding-top: 15px;
    padding-bottom: 13px;
}
"""


# Map icon types → variant → stylesheet
_BTN_VARIANTS = {
    "primary": MESSAGE_BOX_PRIMARY_BTN,
    "danger": MESSAGE_BOX_DANGER_BTN,
    "cancel": MESSAGE_BOX_CANCEL_BTN,
}


class ThemedMessageBox(QDialog):

    def __init__(self, parent=None, icon_type="info"):
        super().__init__(parent)
        self.setWindowTitle("Study Master")
        self.setModal(True)
        self.setMinimumWidth(560)
        self.setMinimumHeight(260)
        self.resize(620, 320)
        self.setStyleSheet(MESSAGE_BOX_DIALOG)

        # Celebration (used only by success())
        self._celebration = CelebrationAnimation()
        self._celebration.hide()

        # ── Icon — bigger, cleaner
        self._icon_label = QLabel()
        self._icon_label.setFixedSize(80, 80)
        self._icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # ── Title (now visible for every dialog)
        self._title_label = QLabel()
        self._title_label.setWordWrap(True)
        self._title_label.setStyleSheet(MESSAGE_BOX_TITLE)

        # ── Text
        self._text_label = QLabel()
        self._text_label.setWordWrap(True)
        self._text_label.setStyleSheet(MESSAGE_BOX_TEXT)

        # ── Button row
        self._button_row = QHBoxLayout()
        self._button_row.setSpacing(12)

        # ── Layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(36, 32, 36, 28)
        main_layout.setSpacing(24)

        content_row = QHBoxLayout()
        content_row.setSpacing(24)
        content_row.addWidget(
            self._celebration,
            alignment=Qt.AlignmentFlag.AlignCenter,
        )
        content_row.addWidget(
            self._icon_label,
            alignment=Qt.AlignmentFlag.AlignTop,
        )

        text_col = QVBoxLayout()
        text_col.setSpacing(8)
        text_col.addWidget(self._title_label)
        text_col.addWidget(self._text_label)
        text_col.addStretch()
        content_row.addLayout(text_col, 1)

        main_layout.addLayout(content_row, 1)
        main_layout.addLayout(self._button_row)

        self._set_icon(icon_type)
        self._icon_type = icon_type

    # ─────────────────────────────────────────
    def _set_icon(self, icon_type):
        style = self.style()
        icon_map = {
            "info": QStyle.StandardPixmap.SP_MessageBoxInformation,
            "question": QStyle.StandardPixmap.SP_MessageBoxQuestion,
            "warning": QStyle.StandardPixmap.SP_MessageBoxWarning,
            "error": QStyle.StandardPixmap.SP_MessageBoxCritical,
        }
        if icon_type in icon_map:
            self._icon_label.setPixmap(
                style.standardIcon(icon_map[icon_type]).pixmap(72, 72)
            )
        else:
            self._icon_label.hide()

    # ─────────────────────────────────────────
    def _add_button(self, text, role, variant="primary", fancy=False):
        button = QPushButton(text)
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.clicked.connect(lambda: self.done(role))

        if fancy:
            button.setStyleSheet(SUCCESS_BUTTON_STYLE)
            button.setMinimumWidth(180)
            button.setMinimumHeight(52)
            shadow = QGraphicsDropShadowEffect(button)
            shadow.setBlurRadius(24)
            shadow.setColor(QColor(34, 197, 94, 140))
            shadow.setOffset(0, 6)
            button.setGraphicsEffect(shadow)
        else:
            button.setStyleSheet(_BTN_VARIANTS.get(variant, MESSAGE_BOX_PRIMARY_BTN))

        self._button_row.addWidget(button)

    # ─────────────────────────────────────────
    @staticmethod
    def _show(parent, title, text, icon_type, buttons):
        dialog = ThemedMessageBox(parent, icon_type)
        dialog._title_label.setText(title)
        dialog._text_label.setText(text)
        for btn_text, role, variant in buttons:
            dialog._add_button(btn_text, role, variant)

        if icon_type == "error":
            SoundManager.play_error()
        elif icon_type == "warning":
            SoundManager.play_warning()
        elif icon_type == "info":
            SoundManager.play_info()

        return dialog.exec()

    # ─────────────────────────────────────────
    @staticmethod
    def success(parent, title, text):
        dialog = ThemedMessageBox(parent, "info")
        dialog._title_label.setText(title)
        dialog._text_label.setText(text)
        dialog._icon_label.hide()
        dialog._celebration.show()
        dialog._add_button("Awesome! 🎉", 1, fancy=True)
        QTimer.singleShot(50, dialog._celebration.start)
        SoundManager.play_success()
        return dialog.exec()

    # ─────────────────────────────────────────
    @staticmethod
    def info(parent, title, text):
        return ThemedMessageBox._show(
            parent, title, text, "info",
            [("OK", 1, "primary")],
        )

    @staticmethod
    def warning(parent, title, text):
        return ThemedMessageBox._show(
            parent, title, text, "warning",
            [("OK", 1, "primary")],
        )

    @staticmethod
    def error(parent, title, text):
        return ThemedMessageBox._show(
            parent, title, text, "error",
            [("OK", 1, "primary")],
        )

    @staticmethod
    def question(parent, title, text):
        return ThemedMessageBox._show(
            parent, title, text, "question",
            [("Yes", 1, "primary"), ("No", 0, "cancel")],
        ) == 1

    # ── New: for delete confirmations ──
    @staticmethod
    def confirm_danger(parent, title, text, confirm_text="Delete"):
        return ThemedMessageBox._show(
            parent, title, text, "warning",
            [(confirm_text, 1, "danger"), ("Cancel", 0, "cancel")],
        ) == 1