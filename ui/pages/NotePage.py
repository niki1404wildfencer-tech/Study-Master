from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor
from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QFrame, QDialog,
    QScrollArea, QListWidget, QListWidgetItem,
    QSizePolicy, QTextEdit
)

from ui.components.MessageBox import ThemedMessageBox

from ui.styles.colors import PRIMARY, ERROR, TEXT_SECONDARY
from ui.styles.spacing import SMALL, MEDIUM, LARGE
from ui.styles.styles import (
    search_bar,
    Add_btn,
    card_style,
    card_hover_style,
    NOTE_PAGE_TITLE,
    NOTE_CARD_TITLE,
    NOTE_TEMPLATE_TITLE,
    NOTE_DELETE_BUTTON,
    note_content,
    selector_label_style,
    selector_shared,
    DIALOG_STYLE,
    DIALOG_CANCEL_BTN,
    FOLDER_PANEL,
    FOLDER_LIST,
)

from assets.icon.icon import ADD, DELETE, EDIT

from widgets.NoteInput import AddNote, FolderInput

from managers.NoteManager import NoteManager
from managers.SubjectManager import SubjectManager
from managers.TaskManager import TaskManager


# ───────────────────────────────────────────────────────
def _color_dot_icon(color, size=14):
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)
    p = QPainter(pixmap)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    p.setBrush(QColor(color))
    p.setPen(Qt.PenStyle.NoPen)
    p.drawRoundedRect(0, 0, size, size, 4, 4)
    p.end()
    return QIcon(pixmap)


def _rgba(hex_color, alpha=0.14):
    try:
        h = hex_color.lstrip("#")
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        return f"rgba({r}, {g}, {b}, {alpha})"
    except Exception:
        return f"rgba(79, 124, 255, {alpha})"


def _make_chip(text, color):
    lbl = QLabel(text)
    lbl.setStyleSheet(
        f"QLabel {{"
        f" background: {_rgba(color, 0.14)};"
        f" color: {color};"
        f" border-radius: 8px;"
        f" padding: 3px 10px;"
        f' font-family: "Segoe UI", "Vazirmatn";'
        f" font-size: 11px;"
        f" font-weight: 700;"
        f"}}"
    )
    return lbl


# ═══════════════════════════════════════════════════════
# Note Viewer Dialog
# ═══════════════════════════════════════════════════════
class NoteViewer(QDialog):

    edit_requested = Signal(int)

    def __init__(self, note, subject=None, task=None, folder=None, parent=None):
        super().__init__(parent)
        self.note = note
        self.setWindowTitle(note.get("title", "Note"))
        self.setModal(True)
        self.resize(720, 640)
        self.setMinimumSize(560, 480)
        self.setStyleSheet(DIALOG_STYLE)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(LARGE, LARGE, LARGE, LARGE)
        layout.setSpacing(MEDIUM)

        # ── Title
        title = QLabel(note.get("title", "Untitled"))
        title.setWordWrap(True)
        title.setStyleSheet(NOTE_PAGE_TITLE)
        layout.addWidget(title)

        # ── Chips row
        chips_row = QHBoxLayout()
        chips_row.setSpacing(SMALL)

        if folder:
            chips_row.addWidget(
                _make_chip(folder["name"], folder.get("color", PRIMARY))
            )
        if subject:
            chips_row.addWidget(
                _make_chip(subject["name"], subject.get("color", PRIMARY))
            )
        if task:
            chips_row.addWidget(_make_chip(task["name"], "#6B7280"))

        chips_row.addStretch()

        updated = note.get("updated_at", note.get("created_at", ""))
        if updated:
            try:
                from datetime import datetime
                dt = datetime.fromisoformat(updated)
                stamp = dt.strftime("%d %b %Y")
            except Exception:
                stamp = ""
            if stamp:
                ts = QLabel(stamp)
                ts.setStyleSheet(
                    f"QLabel {{"
                    f" background: transparent;"
                    f" color: #9CA3AF;"
                    f' font-family: "Segoe UI", "Vazirmatn";'
                    f" font-size: 12px;"
                    f"}}"
                )
                chips_row.addWidget(ts)

        layout.addLayout(chips_row)

        # ── Separator
        sep = QFrame()
        sep.setFixedHeight(1)
        sep.setStyleSheet("background: #E4E8F0; border: none;")
        layout.addWidget(sep)

        # ── Content
        self.content_area = QTextEdit()
        self.content_area.setReadOnly(True)
        self.content_area.setPlainText(note.get("content", ""))
        self.content_area.setStyleSheet(
            f"QTextEdit {{"
            f" background: transparent;"
            f" border: none;"
            f" color: #1F2937;"
            f' font-family: "Patrick Hand", "Vazirmatn";'
            f" font-size: 20px;"
            f" padding: 0;"
            f"}}"
        )
        layout.addWidget(self.content_area, 1)

        # ── Buttons
        btn_row = QHBoxLayout()
        btn_row.addStretch()

        self.edit_btn = QPushButton("  Edit")
        self.edit_btn.setIcon(QIcon(str(EDIT)))
        self.edit_btn.setIconSize(QSize(18, 18))
        self.edit_btn.setFixedSize(140, 56)
        self.edit_btn.setStyleSheet(Add_btn)
        self.edit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.edit_btn.clicked.connect(self._on_edit)

        self.close_btn = QPushButton("Close")
        self.close_btn.setObjectName("dialogCancelBtn")
        self.close_btn.setFixedSize(140, 56)
        self.close_btn.setStyleSheet(DIALOG_CANCEL_BTN)
        self.close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.close_btn.clicked.connect(self.reject)

        btn_row.addWidget(self.close_btn)
        btn_row.addWidget(self.edit_btn)
        layout.addLayout(btn_row)

    def _on_edit(self):
        note_id = self.note.get("id")
        self.accept()
        if note_id is not None:
            self.edit_requested.emit(note_id)


# ═══════════════════════════════════════════════════════
# Note Card
# ═══════════════════════════════════════════════════════
class NoteCard(QFrame):

    edit_requested = Signal(int)
    delete_requested = Signal(int)
    view_requested = Signal(int)

    def __init__(self, note, subject=None, task=None, folder=None, parent=None):
        super().__init__(parent)
        self.note = note

        self.setObjectName("NoteCard")
        self.setMinimumHeight(130)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        if folder:
            accent = folder.get("color", PRIMARY)
        elif subject:
            accent = subject.get("color", PRIMARY)
        else:
            accent = "#94A3B8"

        outer = QHBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        stripe = QFrame()
        stripe.setFixedWidth(5)
        stripe.setStyleSheet(
            f"background: {accent};"
            "border-top-left-radius: 16px;"
            "border-bottom-left-radius: 16px;"
        )
        outer.addWidget(stripe)

        wrap = QWidget()
        wrap.setStyleSheet("background: transparent;")
        outer.addWidget(wrap, 1)

        content = QVBoxLayout(wrap)
        content.setContentsMargins(LARGE, MEDIUM + 4, LARGE, MEDIUM + 4)
        content.setSpacing(SMALL)

        title_lbl = QLabel(note.get("title", "Untitled"))
        title_lbl.setWordWrap(True)
        title_lbl.setStyleSheet(NOTE_TEMPLATE_TITLE)
        content.addWidget(title_lbl)

        raw = note.get("content", "").strip().replace("\n", "  ")
        preview = raw if len(raw) <= 180 else raw[:180].rstrip() + "…"
        preview_lbl = QLabel(preview or "—")
        preview_lbl.setWordWrap(True)
        preview_lbl.setStyleSheet(note_content)
        content.addWidget(preview_lbl)

        footer = QHBoxLayout()
        footer.setSpacing(8)

        if folder:
            footer.addWidget(
                _make_chip(folder["name"], folder.get("color", PRIMARY))
            )
        if subject:
            footer.addWidget(
                _make_chip(subject["name"], subject.get("color", PRIMARY))
            )
        if task:
            footer.addWidget(_make_chip(task["name"], "#6B7280"))

        footer.addStretch()

        updated = note.get("updated_at", note.get("created_at", ""))
        if updated:
            try:
                from datetime import datetime
                dt = datetime.fromisoformat(updated)
                stamp = dt.strftime("%d %b %Y")
            except Exception:
                stamp = ""
            if stamp:
                ts = QLabel(stamp)
                ts.setStyleSheet(
                    f"QLabel {{"
                    f" background: transparent;"
                    f" color: #9CA3AF;"
                    f' font-family: "Segoe UI", "Vazirmatn";'
                    f" font-size: 11px;"
                    f"}}"
                )
                footer.addWidget(ts)

        # ── Icon buttons ──
        edit_btn = QPushButton()
        edit_btn.setIcon(QIcon(str(EDIT)))
        edit_btn.setIconSize(QSize(16, 16))
        edit_btn.setFixedSize(34, 34)
        edit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        edit_btn.setStyleSheet(selector_shared)
        edit_btn.setToolTip("Edit note")
        edit_btn.clicked.connect(
            lambda: self.edit_requested.emit(self.note["id"])
        )

        del_btn = QPushButton()
        del_btn.setIcon(QIcon(str(DELETE)))
        del_btn.setIconSize(QSize(16, 16))
        del_btn.setFixedSize(34, 34)
        del_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        del_btn.setStyleSheet(NOTE_DELETE_BUTTON)
        del_btn.setToolTip("Delete note")
        del_btn.clicked.connect(
            lambda: self.delete_requested.emit(self.note["id"])
        )

        footer.addWidget(edit_btn)
        footer.addWidget(del_btn)

        content.addLayout(footer)

        self.setStyleSheet(card_style)

    def enterEvent(self, event):
        self.setStyleSheet(card_hover_style)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setStyleSheet(card_style)
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        # Clicking anywhere except the buttons opens the viewer.
        # QPushButton consumes its own clicks, so this only fires
        # for clicks on labels, chips, the stripe, and empty space.
        if event.button() == Qt.MouseButton.LeftButton:
            self.view_requested.emit(self.note["id"])
            event.accept()
            return
        super().mousePressEvent(event)


# ═══════════════════════════════════════════════════════
# Notes Page
# ═══════════════════════════════════════════════════════
class NotesPage(QWidget):

    search_requested = Signal(str)
    add_requested = Signal()

    ALL_FOLDER_ID = "all"
    UNCATEGORIZED_ID = None

    def __init__(self):
        super().__init__()

        self.note_manager = NoteManager()
        self.subject_manager = SubjectManager()
        self.task_manager = TaskManager()

        self.current_folder_id = self.ALL_FOLDER_ID

        self.setup_ui()
        self.connect_signals()
        self.refresh_folders()
        self.refresh_notes()

    def setup_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(LARGE, LARGE, LARGE, LARGE)
        root.setSpacing(MEDIUM)

        title = QLabel("Notes")
        title.setStyleSheet(NOTE_PAGE_TITLE)
        root.addWidget(title)

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search notes...")
        self.search_bar.setFixedHeight(54)
        self.search_bar.setStyleSheet(search_bar)
        root.addWidget(self.search_bar)

        body = QHBoxLayout()
        body.setSpacing(MEDIUM)

        # ── Left: folder panel ──
        folder_panel = QFrame()
        folder_panel.setObjectName("folderPanel")
        folder_panel.setFixedWidth(240)
        folder_panel.setStyleSheet(FOLDER_PANEL)

        fp = QVBoxLayout(folder_panel)
        fp.setContentsMargins(MEDIUM, MEDIUM, MEDIUM, MEDIUM)
        fp.setSpacing(SMALL)

        section = QLabel("FOLDERS")
        section.setStyleSheet(selector_label_style)
        fp.addWidget(section)

        self.folder_list = QListWidget()
        self.folder_list.setStyleSheet(FOLDER_LIST)
        self.folder_list.setFixedHeight(320)
        fp.addWidget(self.folder_list)

        # ── New Folder — icon + text, taller so nothing clips
        self.new_folder_btn = QPushButton("  New Folder")
        self.new_folder_btn.setIcon(QIcon(str(ADD)))
        self.new_folder_btn.setIconSize(QSize(20, 20))
        self.new_folder_btn.setFixedHeight(50)
        self.new_folder_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.new_folder_btn.setStyleSheet(Add_btn)

        # ── Rename — icon + text
        self.rename_folder_btn = QPushButton("  Rename")
        self.rename_folder_btn.setIcon(QIcon(str(EDIT)))
        self.rename_folder_btn.setIconSize(QSize(16, 16))
        self.rename_folder_btn.setFixedHeight(48)
        self.rename_folder_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.rename_folder_btn.setStyleSheet(Add_btn)
        

        # ── Delete — icon + text, red
        self.delete_folder_btn = QPushButton("  Delete")
        self.delete_folder_btn.setIcon(QIcon(str(DELETE)))
        self.delete_folder_btn.setIconSize(QSize(16, 16))
        self.delete_folder_btn.setFixedHeight(46)
        self.delete_folder_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.delete_folder_btn.setStyleSheet(NOTE_DELETE_BUTTON)

        fp.addWidget(self.new_folder_btn)
        fp.addSpacing(4)
        fp.addWidget(self.rename_folder_btn)
        fp.addWidget(self.delete_folder_btn)
        fp.addStretch()

        body.addWidget(folder_panel)

        # ── Right: notes area ──
        right = QWidget()
        right.setStyleSheet("background: transparent;")
        rl = QVBoxLayout(right)
        rl.setContentsMargins(0, 0, 0, 0)
        rl.setSpacing(MEDIUM)

        header = QHBoxLayout()
        header.setSpacing(MEDIUM)

        self.folder_title = QLabel("All Notes")
        self.folder_title.setStyleSheet(NOTE_CARD_TITLE)
        header.addWidget(self.folder_title)

        self.folder_count = QLabel("(0)")
        self.folder_count.setStyleSheet(selector_label_style)
        header.addWidget(self.folder_count)
        header.addStretch()

        self.add_button = QPushButton("  Add Note")
        self.add_button.setIcon(QIcon(str(ADD)))
        self.add_button.setIconSize(QSize(20, 20))
        self.add_button.setFixedHeight(50)
        self.add_button.setMinimumWidth(180)
        self.add_button.setStyleSheet(Add_btn)
        self.add_button.setCursor(Qt.CursorShape.PointingHandCursor)
        header.addWidget(self.add_button)

        rl.addLayout(header)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll.setStyleSheet(
            "QScrollArea { background: transparent; border: none; }"
            "QScrollArea > QWidget > QWidget { background: transparent; }"
        )

        self.notes_container = QWidget()
        self.notes_layout = QVBoxLayout(self.notes_container)
        self.notes_layout.setContentsMargins(0, 0, 0, 0)
        self.notes_layout.setSpacing(MEDIUM)
        self.notes_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll.setWidget(self.notes_container)

        rl.addWidget(self.scroll, 1)

        self.empty_label = QLabel("No notes in this folder yet.")
        self.empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.empty_label.setStyleSheet(
            f"QLabel {{"
            f" color: #9CA3AF;"
            f' font-family: "Segoe UI", "Vazirmatn";'
            f" font-size: 14px;"
            f" background: transparent;"
            f" padding: 60px 0;"
            f"}}"
        )
        rl.addWidget(self.empty_label)

        body.addWidget(right, 1)
        root.addLayout(body, 1)

        self._update_folder_buttons()

    def connect_signals(self):
        self.search_bar.textChanged.connect(self.on_search)
        self.add_button.clicked.connect(self.add_note)
        self.folder_list.currentItemChanged.connect(self._on_folder_changed)
        self.new_folder_btn.clicked.connect(self.add_folder)
        self.rename_folder_btn.clicked.connect(self.rename_folder)
        self.delete_folder_btn.clicked.connect(self.delete_folder)

    # ── Folders ──

    def refresh_folders(self):
        self.folder_list.blockSignals(True)
        self.folder_list.clear()

        it = QListWidgetItem(_color_dot_icon(PRIMARY, 14), "  All Notes")
        it.setData(Qt.ItemDataRole.UserRole, self.ALL_FOLDER_ID)
        self.folder_list.addItem(it)

        for f in self.note_manager.get_folders():
            it = QListWidgetItem(
                _color_dot_icon(f.get("color", PRIMARY), 14),
                f"  {f['name']}",
            )
            it.setData(Qt.ItemDataRole.UserRole, f["id"])
            self.folder_list.addItem(it)

        unc = self.note_manager.count_notes_by_folder(None)
        if unc > 0:
            it = QListWidgetItem(
                _color_dot_icon("#94A3B8", 14),
                "  Uncategorized",
            )
            it.setData(Qt.ItemDataRole.UserRole, self.UNCATEGORIZED_ID)
            self.folder_list.addItem(it)

        self.folder_list.blockSignals(False)
        self._select_folder(self.current_folder_id)

    def _select_folder(self, folder_id):
        for i in range(self.folder_list.count()):
            it = self.folder_list.item(i)
            if it.data(Qt.ItemDataRole.UserRole) == folder_id:
                self.folder_list.setCurrentItem(it)
                return
        if folder_id != self.ALL_FOLDER_ID:
            self.current_folder_id = self.ALL_FOLDER_ID
            self._select_folder(self.ALL_FOLDER_ID)

    def _on_folder_changed(self, current, previous):
        if current is None:
            return
        self.current_folder_id = current.data(Qt.ItemDataRole.UserRole)
        self._update_folder_buttons()
        self.refresh_notes()

    def _update_folder_buttons(self):
        is_user = isinstance(self.current_folder_id, int)
        self.rename_folder_btn.setEnabled(is_user)
        self.delete_folder_btn.setEnabled(is_user)

    # ── Folders CRUD ──

    def add_folder(self):
        dialog = FolderInput("New Folder", parent=self)
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return
        name, color = dialog.value()
        if not name:
            return
        folder = self.note_manager.add_folder(name, color)
        self.refresh_folders()
        if folder:
            self._select_folder(folder["id"])

    def rename_folder(self):
        if not isinstance(self.current_folder_id, int):
            return
        folder = self.note_manager.get_folder(self.current_folder_id)
        if folder is None:
            return
        dialog = FolderInput(
            "Edit Folder",
            parent=self,
            name=folder["name"],
            color=folder.get("color", PRIMARY),
        )
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return
        name, color = dialog.value()
        if not name:
            return
        self.note_manager.update_folder(folder["id"], name, color)
        self.refresh_folders()
        self.refresh_notes()

    def delete_folder(self):
        if not isinstance(self.current_folder_id, int):
            return
        folder = self.note_manager.get_folder(self.current_folder_id)
        if folder is None:
            return
        count = self.note_manager.count_notes_by_folder(folder["id"])
        msg = f"Delete folder “{folder['name']}”?\n\n" + (
            f"{count} note(s) will move to Uncategorized. No notes will be deleted."
            if count > 0 else "This folder is empty."
        )
        if not ThemedMessageBox.confirm_danger(self, "Delete Folder", msg , "Delete"):
            return
        self.note_manager.delete_folder(folder["id"])
        self.current_folder_id = self.ALL_FOLDER_ID
        self.refresh_folders()
        self.refresh_notes()

    # ── Notes ──

    def on_search(self, text):
        results = self.note_manager.search_notes(
            text, folder_id=self.current_folder_id
        )
        self._render_notes(results)
        self.search_requested.emit(text)

    def view_note(self, note_id):
        note = self.note_manager.get_note(note_id)
        if note is None:
            return

        subject = None
        if note.get("subject_id") is not None:
            subject = self.subject_manager.get_subject(note["subject_id"])

        task = None
        if note.get("task_id") is not None and self.task_manager is not None:
            task = self.task_manager.get_task(note["task_id"])

        folder = None
        if note.get("folder_id") is not None:
            folder = self.note_manager.get_folder(note["folder_id"])

        viewer = NoteViewer(
            note,
            subject=subject,
            task=task,
            folder=folder,
            parent=self,
        )
        viewer.edit_requested.connect(self.edit_note)
        viewer.exec()

    def add_note(self):
        default_folder = (
            self.current_folder_id
            if isinstance(self.current_folder_id, int)
            else None
        )
        dialog = AddNote(
            title="Add Note",
            subject_manager=self.subject_manager,
            task_manager=self.task_manager,
            note_manager=self.note_manager,
            parent=self,
            default_folder_id=default_folder,
        )
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return
        data = dialog.value()
        self.note_manager.add_note(
            title=data["title"],
            content=data["content"],
            subject_id=data["subject_id"],
            task_id=data["task_id"],
            folder_id=data["folder_id"],
        )
        self.refresh_folders()
        self.refresh_notes()
        self.add_requested.emit()

    def edit_note(self, note_id):
        note = self.note_manager.get_note(note_id)
        if note is None:
            return
        dialog = AddNote(
            title="Edit Note",
            subject_manager=self.subject_manager,
            task_manager=self.task_manager,
            note_manager=self.note_manager,
            parent=self,
            note=note,
        )
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return
        data = dialog.value()
        self.note_manager.update_note(
            note_id=note_id,
            title=data["title"],
            content=data["content"],
            subject_id=data["subject_id"],
            task_id=data["task_id"],
            folder_id=data["folder_id"],
        )
        self.refresh_folders()
        self.refresh_notes()

    def delete_note(self, note_id):
        note = self.note_manager.get_note(note_id)
        if note is None:
            return
        if not ThemedMessageBox.confirm_danger(
            self,
            "Delete Note",
            f"Delete “{note.get('title', 'this note')}”?\n\nThis cannot be undone.",
        ):
            return
        self.note_manager.delete_note(note_id)
        self.refresh_folders()
        self.refresh_notes()

    # ── Render ──

    def refresh_notes(self):
        notes = self.note_manager.get_notes_by_folder(self.current_folder_id)

        q = self.search_bar.text().strip()
        if q:
            q_lower = q.lower()
            notes = [
                n for n in notes
                if q_lower in str(n.get("title", "")).lower()
                or q_lower in str(n.get("content", "")).lower()
            ]

        if self.current_folder_id == self.ALL_FOLDER_ID:
            label = "All Notes"
        elif self.current_folder_id is None:
            label = "Uncategorized"
        else:
            folder = self.note_manager.get_folder(self.current_folder_id)
            label = folder["name"] if folder else "Folder"

        self.folder_title.setText(label)
        self.folder_count.setText(f"({len(notes)})")

        self._render_notes(notes)

    def _render_notes(self, notes):
        while self.notes_layout.count():
            item = self.notes_layout.takeAt(0)
            w = item.widget()
            if w is not None:
                w.deleteLater()

        if not notes:
            self.scroll.setVisible(False)
            self.empty_label.setVisible(True)
            return

        self.scroll.setVisible(True)
        self.empty_label.setVisible(False)

        subjects = {s["id"]: s for s in self.subject_manager.get_subjects()}
        folders = {f["id"]: f for f in self.note_manager.get_folders()}

        for note in notes:
            subject = subjects.get(note.get("subject_id"))
            folder = folders.get(note.get("folder_id"))
            task = None
            if note.get("task_id") is not None and self.task_manager is not None:
                task = self.task_manager.get_task(note["task_id"])

            card = NoteCard(note, subject=subject, task=task, folder=folder)
            card.edit_requested.connect(self.edit_note)
            card.delete_requested.connect(self.delete_note)
            card.view_requested.connect(self.view_note)
            self.notes_layout.addWidget(card)