from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor
from PySide6.QtWidgets import (
    QDialog, QLabel, QVBoxLayout, QHBoxLayout,
    QComboBox, QLineEdit, QPushButton,
)

from ui.styles.spacing import MEDIUM, LARGE
from ui.styles.styles import (
    DIALOG_STYLE,
    COMBO_BOX,
    NOTE_DIALOG_HEADER,
    NOTE_FORM_LABEL,
    DIALOG_CANCEL_BTN,
    Add_btn,
)
from ui.components.MessageBox import ThemedMessageBox

from managers.SubjectManager import SubjectManager
from managers.TaskManager import TaskManager


PRIORITIES = [
    {"key": "critical", "label": "Critical", "color": "#EF4444"},
    {"key": "high",     "label": "High",     "color": "#F97316"},
    {"key": "medium",   "label": "Medium",   "color": "#FACC15"},
    {"key": "low",      "label": "Low",      "color": "#22C55E"},
]


def _dot_icon(color, size=12):
    pix = QPixmap(size, size)
    pix.fill(Qt.GlobalColor.transparent)
    p = QPainter(pix)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    p.setBrush(QColor(color))
    p.setPen(Qt.PenStyle.NoPen)
    p.drawEllipse(0, 0, size, size)
    p.end()
    return QIcon(pix)


class AddTaskDialog(QDialog):
    """
    Shared Add/Edit Task dialog.
    Used by:
      - Timer  →  TaskSelector
      - Planner
    """

    def __init__(
        self,
        parent=None,
        task=None,
        default_subject_id=None,
        default_priority="medium",
    ):
        super().__init__(parent)

        self.task = task
        self.default_subject_id = default_subject_id
        self.default_priority = default_priority

        self.subject_manager = SubjectManager()

        self.setWindowTitle("Edit Task" if task else "Add Task")
        self.setModal(True)
        self.resize(520, 500)
        self.setMinimumSize(480, 460)
        self.setStyleSheet(DIALOG_STYLE)

        self.setup_ui()
        self.load_subjects()

        if task is not None:
            self.load_task()
        elif default_subject_id is not None:
            idx = self.subject_combo.findData(default_subject_id)
            if idx >= 0:
                self.subject_combo.setCurrentIndex(idx)

        self.connect_signals()

    # =====================================================
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(LARGE, LARGE, LARGE, LARGE)
        layout.setSpacing(MEDIUM)

        header = QLabel("Edit Task" if self.task else "Add Task")
        header.setStyleSheet(NOTE_DIALOG_HEADER)
        layout.addWidget(header)

        # Subject
        self.subject_label = QLabel("Subject")
        self.subject_label.setStyleSheet(NOTE_FORM_LABEL)
        layout.addWidget(self.subject_label)

        self.subject_combo = QComboBox()
        self.subject_combo.setStyleSheet(COMBO_BOX)
        self.subject_combo.setFixedHeight(48)
        layout.addWidget(self.subject_combo)

        # Name
        self.name_label = QLabel("Task name")
        self.name_label.setStyleSheet(NOTE_FORM_LABEL)
        layout.addWidget(self.name_label)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e.g. Finish chapter 3...")
        self.name_input.setFixedHeight(48)
        layout.addWidget(self.name_input)

        # Priority
        self.priority_label = QLabel("Priority")
        self.priority_label.setStyleSheet(NOTE_FORM_LABEL)
        layout.addWidget(self.priority_label)

        self.priority_combo = QComboBox()
        self.priority_combo.setStyleSheet(COMBO_BOX)
        self.priority_combo.setFixedHeight(48)
        for p in PRIORITIES:
            self.priority_combo.addItem(
                _dot_icon(p["color"]),
                p["label"],
                p["key"],
            )
        idx = self.priority_combo.findData(self.default_priority)
        if idx >= 0:
            self.priority_combo.setCurrentIndex(idx)
        layout.addWidget(self.priority_combo)

        layout.addStretch()

        # Buttons
        row = QHBoxLayout()
        row.setSpacing(MEDIUM)
        row.addStretch()

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setObjectName("dialogCancelBtn")
        self.cancel_button.setFixedSize(140, 56)
        self.cancel_button.setStyleSheet(DIALOG_CANCEL_BTN)
        self.cancel_button.setCursor(Qt.CursorShape.PointingHandCursor)

        self.save_button = QPushButton("Save")
        self.save_button.setFixedSize(140, 56)
        self.save_button.setStyleSheet(Add_btn)
        self.save_button.setCursor(Qt.CursorShape.PointingHandCursor)

        row.addWidget(self.cancel_button)
        row.addWidget(self.save_button)
        layout.addLayout(row)

    # =====================================================
    def load_subjects(self):
        self.subject_combo.clear()
        self.subject_combo.addItem("— Select Subject —", None)
        for s in self.subject_manager.get_subjects():
            self.subject_combo.addItem(s["name"], s["id"])

    def load_task(self):
        self.name_input.setText(self.task.get("name", ""))

        sid = self.task.get("subject_id")
        if sid is not None:
            idx = self.subject_combo.findData(sid)
            if idx >= 0:
                self.subject_combo.setCurrentIndex(idx)

        pri = self.task.get("priority", "medium")
        idx = self.priority_combo.findData(pri)
        if idx >= 0:
            self.priority_combo.setCurrentIndex(idx)

    # =====================================================
    def connect_signals(self):
        self.cancel_button.clicked.connect(self.reject)
        self.save_button.clicked.connect(self._on_save)

    def _on_save(self):
        name = self.name_input.text().strip()
        if not name:
            self.name_input.setFocus()
            return

        subject_id = self.subject_combo.currentData()
        if subject_id is None:
            ThemedMessageBox.warning(
                self,
                "Subject required",
                "Please pick a subject for this task.",
            )
            return

        self._result = {
            "name": name,
            "subject_id": subject_id,
            "priority": self.priority_combo.currentData(),
        }
        self.accept()

    def value(self):
        return getattr(self, "_result", None)