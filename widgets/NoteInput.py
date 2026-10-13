from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog, QLabel, QVBoxLayout, QHBoxLayout, QComboBox,
    QLineEdit, QTextEdit, QPushButton, QColorDialog,
)

from ui.styles.styles import (
    DIALOG_STYLE,
    COMBO_BOX,
    NOTE_DIALOG_HEADER,
    NOTE_FORM_LABEL,
    NOTE_CONTENT_INPUT,
    SESSION_BUTTON,
    selector_shared,
    Add_btn,
    DIALOG_CANCEL_BTN,
)
from ui.styles.radius import BUTTON_RADIUS
from ui.styles.fonts import FONT_STACK
from ui.styles.spacing import SMALL, MEDIUM, LARGE


# ═══════════════════════════════════════════════════════
# Folder Add / Edit Dialog
# ═══════════════════════════════════════════════════════
class FolderInput(QDialog):

    def __init__(self, title="Add Folder", parent=None, name="", color="#4F7CFF"):
        super().__init__(parent)
        self.selected_color = color

        self.setWindowTitle(title)
        self.setModal(True)
        self.resize(520, 440)
        self.setMinimumSize(480, 400)
        self.setStyleSheet(DIALOG_STYLE)

        self.setup_ui(name)
        self.connect_signals()

    def setup_ui(self, name):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(LARGE, LARGE, LARGE, LARGE)
        layout.setSpacing(MEDIUM)

        self.header = QLabel("Folder")
        self.header.setStyleSheet(NOTE_DIALOG_HEADER)
        layout.addWidget(self.header)

        self.name_label = QLabel("Folder name")
        self.name_label.setStyleSheet(NOTE_FORM_LABEL)
        layout.addWidget(self.name_label)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e.g. Math, Physics, Ideas...")
        self.name_input.setText(name)
        self.name_input.setFixedHeight(48)
        layout.addWidget(self.name_input)

        self.color_label = QLabel("Folder color")
        self.color_label.setStyleSheet(NOTE_FORM_LABEL)
        layout.addWidget(self.color_label)

        # Fixed height so it never expands and eats the dialog
        self.color_button = QPushButton("Choose color")
        self.color_button.setFixedHeight(52)
        self.color_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.update_color_button()
        layout.addWidget(self.color_button)

        layout.addStretch()

        row = QHBoxLayout()
        row.setSpacing(MEDIUM)
        row.addStretch()

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setObjectName("dialogCancelBtn")
        self.cancel_button.setFixedHeight(56)
        self.cancel_button.setMaximumWidth(140)
        self.cancel_button.setStyleSheet(DIALOG_CANCEL_BTN)
        self.cancel_button.setCursor(Qt.CursorShape.PointingHandCursor)

        self.save_button = QPushButton("Save")
        self.save_button.setFixedHeight(56)
        self.save_button.setMaximumWidth(140)
        self.save_button.setStyleSheet(Add_btn)
        self.save_button.setCursor(Qt.CursorShape.PointingHandCursor)

        row.addWidget(self.cancel_button)
        row.addWidget(self.save_button)
        layout.addLayout(row)

    def connect_signals(self):
        self.color_button.clicked.connect(self.choose_color)
        self.save_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

    def choose_color(self):
        color = QColorDialog.getColor(parent=self, title="Choose Folder Color")
        if not color.isValid():
            return
        self.selected_color = color.name()
        self.update_color_button()

    def update_color_button(self):
        # inline: color is a runtime value from QColorDialog
        self.color_button.setStyleSheet(
            f"QPushButton {{"
            f" background-color: {self.selected_color};"
            f" color: white;"
            f" border: 2px solid rgba(255, 255, 255, 0.35);"
            f" border-radius: {BUTTON_RADIUS}px;"
            f" padding: 8px 20px;"
            f" font-family: {FONT_STACK};"
            f" font-size: 14px;"
            f" font-weight: 700;"
            f"}}"
            f"QPushButton:hover {{"
            f" border: 2px solid white;"
            f"}}"
        )

    def value(self):
        return (self.name_input.text().strip(), self.selected_color)


# ═══════════════════════════════════════════════════════
# Note Add / Edit Dialog (unchanged)
# ═══════════════════════════════════════════════════════
class AddNote(QDialog):

    def __init__(
        self,
        title="Add Note",
        subject_manager=None,
        task_manager=None,
        note_manager=None,
        parent=None,
        note=None,
        default_folder_id=None,
    ):
        super().__init__(parent)

        self.subject_manager = subject_manager
        self.task_manager = task_manager
        self.note_manager = note_manager
        self.note = note
        self.default_folder_id = default_folder_id

        self.setWindowTitle(title)
        self.setModal(True)
        self.resize(760, 700)
        self.setMinimumSize(680, 600)
        self.setStyleSheet(DIALOG_STYLE)

        self.setup_ui()
        self.load_subjects()
        self.load_folders()

        if self.note is not None:
            self.load_note()
        elif self.default_folder_id is not None:
            idx = self.folder_combo.findData(self.default_folder_id)
            if idx >= 0:
                self.folder_combo.setCurrentIndex(idx)

        self.connect_signals()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(LARGE, LARGE, LARGE, LARGE)
        layout.setSpacing(MEDIUM)

        self.header = QLabel("Edit Note" if self.note else "Add Note")
        self.header.setStyleSheet(NOTE_DIALOG_HEADER)
        layout.addWidget(self.header)

        self.folder_label = QLabel("Folder")
        self.folder_label.setStyleSheet(NOTE_FORM_LABEL)
        layout.addWidget(self.folder_label)

        self.folder_combo = QComboBox()
        self.folder_combo.setStyleSheet(COMBO_BOX)
        self.folder_combo.setFixedHeight(48)
        layout.addWidget(self.folder_combo)

        row = QHBoxLayout()
        row.setSpacing(MEDIUM)

        s_col = QVBoxLayout()
        s_col.setSpacing(SMALL)
        self.subject_label = QLabel("Subject (Optional)")
        self.subject_label.setStyleSheet(NOTE_FORM_LABEL)
        self.subject_combo = QComboBox()
        self.subject_combo.setStyleSheet(COMBO_BOX)
        self.subject_combo.setFixedHeight(48)
        s_col.addWidget(self.subject_label)
        s_col.addWidget(self.subject_combo)

        t_col = QVBoxLayout()
        t_col.setSpacing(SMALL)
        self.task_label = QLabel("Task (Optional)")
        self.task_label.setStyleSheet(NOTE_FORM_LABEL)
        self.task_combo = QComboBox()
        self.task_combo.setStyleSheet(COMBO_BOX)
        self.task_combo.setFixedHeight(48)
        t_col.addWidget(self.task_label)
        t_col.addWidget(self.task_combo)

        row.addLayout(s_col, 1)
        row.addLayout(t_col, 1)
        layout.addLayout(row)

        self.title_label = QLabel("Title")
        self.title_label.setStyleSheet(NOTE_FORM_LABEL)
        layout.addWidget(self.title_label)

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Enter note title...")
        self.title_input.setFixedHeight(50)
        layout.addWidget(self.title_input)

        self.content_label = QLabel("Content")
        self.content_label.setStyleSheet(NOTE_FORM_LABEL)
        layout.addWidget(self.content_label)

        self.content_input = QTextEdit()
        self.content_input.setPlaceholderText("Write your note...")
        self.content_input.setStyleSheet(NOTE_CONTENT_INPUT)
        layout.addWidget(self.content_input, 1)

        row2 = QHBoxLayout()
        row2.setSpacing(MEDIUM)
        row2.addStretch()

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setObjectName("dialogCancelBtn")
        self.cancel_button.setFixedHeight(56)
        self.cancel_button.setMinimumWidth(140)
        self.cancel_button.setStyleSheet(DIALOG_CANCEL_BTN)
        self.cancel_button.setCursor(Qt.CursorShape.PointingHandCursor)

        self.save_button = QPushButton("Save")
        self.save_button.setFixedHeight(56)
        self.save_button.setMinimumWidth(140)
        self.save_button.setStyleSheet(Add_btn)
        self.save_button.setCursor(Qt.CursorShape.PointingHandCursor)
        row2.addWidget(self.cancel_button)
        row2.addWidget(self.save_button)
        layout.addLayout(row2)

    def connect_signals(self):
        self.subject_combo.currentIndexChanged.connect(self.on_subject_changed)
        self.cancel_button.clicked.connect(self.reject)
        self.save_button.clicked.connect(self.save_note)

    def load_subjects(self):
        self.subject_combo.clear()
        self.subject_combo.addItem("No Subject", None)
        if self.subject_manager is None:
            return
        for s in self.subject_manager.get_subjects():
            self.subject_combo.addItem(s["name"], s["id"])

    def load_folders(self):
        self.folder_combo.clear()
        self.folder_combo.addItem("No Folder", None)
        if self.note_manager is None:
            return
        for f in self.note_manager.get_folders():
            self.folder_combo.addItem(f["name"], f["id"])

    def load_tasks(self, subject_id):
        self.task_combo.clear()
        self.task_combo.addItem("No Task", None)
        if subject_id is None or self.task_manager is None:
            return
        for t in self.task_manager.get_tasks(subject_id):
            self.task_combo.addItem(t["name"], t["id"])

    def on_subject_changed(self):
        self.load_tasks(self.subject_combo.currentData())

    def load_note(self):
        self.title_input.setText(self.note.get("title", ""))
        self.content_input.setPlainText(self.note.get("content", ""))

        fid = self.note.get("folder_id")
        if fid is not None:
            idx = self.folder_combo.findData(fid)
            if idx >= 0:
                self.folder_combo.setCurrentIndex(idx)

        sid = self.note.get("subject_id")
        if sid is not None:
            idx = self.subject_combo.findData(sid)
            if idx >= 0:
                self.subject_combo.setCurrentIndex(idx)
        self.load_tasks(sid)

        tid = self.note.get("task_id")
        if tid is not None:
            idx = self.task_combo.findData(tid)
            if idx >= 0:
                self.task_combo.setCurrentIndex(idx)

    def save_note(self):
        title = self.title_input.text().strip()
        content = self.content_input.toPlainText().strip()
        if not title:
            self.title_input.setFocus()
            return
        self._title = title
        self._content = content
        self._subject_id = self.subject_combo.currentData()
        self._task_id = self.task_combo.currentData()
        self._folder_id = self.folder_combo.currentData()
        self.accept()

    def value(self):
        return {
            "title": getattr(self, "_title", ""),
            "content": getattr(self, "_content", ""),
            "subject_id": getattr(self, "_subject_id", None),
            "task_id": getattr(self, "_task_id", None),
            "folder_id": getattr(self, "_folder_id", None),
        }