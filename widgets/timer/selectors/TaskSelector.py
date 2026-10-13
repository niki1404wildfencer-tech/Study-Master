from PySide6.QtCore import (
    Qt,
    Signal,
    QSize,
)

from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QComboBox,
    QPushButton,
    QHBoxLayout,
    QDialog,
)

from PySide6.QtGui import QIcon

from assets.icon.icon import ADD

from ui.styles.styles import (
    COMBO_BOX,
    selector_label_style,
    Add_btn,
)

from widgets.AddTaskDialog import AddTaskDialog


class TaskSelector(QWidget):

    task_changed = Signal(int)

    def __init__(self):
        super().__init__()
        self.current_subject = None
        self.task_manager = None

        self.setup_ui()
        self.connect_signals()

    # =====================================================
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        self.title = QLabel("Task")
        self.title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.title.setStyleSheet(selector_label_style)

        self.combo = QComboBox()
        self.combo.setStyleSheet(COMBO_BOX)
        self.combo.setMinimumHeight(42)

        self.add_btn = QPushButton("Add")
        self.edit_btn = QPushButton("Edit")
        self.delete_btn = QPushButton("Delete")

        self.add_btn.setStyleSheet(Add_btn)
        self.edit_btn.setStyleSheet(Add_btn)
        self.delete_btn.setStyleSheet(Add_btn)

        self.add_btn.setIcon(QIcon(str(ADD)))
        self.add_btn.setIconSize(QSize(40, 40))
        self.add_btn.setFixedSize(140, 52)
        self.edit_btn.setFixedSize(100, 52)
        self.delete_btn.setFixedSize(120, 52)

        row = QHBoxLayout()
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(8)
        row.addWidget(self.combo)
        row.addWidget(self.add_btn)
        row.addWidget(self.edit_btn)
        row.addWidget(self.delete_btn)

        layout.addWidget(self.title)
        layout.addLayout(row)
        self.setLayout(layout)

    def connect_signals(self):
        self.combo.currentIndexChanged.connect(self._on_task_changed)
        self.add_btn.clicked.connect(self.add_task)
        self.edit_btn.clicked.connect(self.edit_task)
        self.delete_btn.clicked.connect(self.delete_task)

    def _on_task_changed(self, index):
        task_id = self.current_task_id()
        if task_id is None:
            return
        self.task_changed.emit(task_id)

    # =====================================================
    # MANAGER
    # =====================================================

    def set_manager(self, manager):
        self.task_manager = manager
        # live-sync with Planner / Dashboard / anywhere else
        try:
            self.task_manager.task_changed.connect(self.refresh)
        except (TypeError, RuntimeError):
            pass

    # =====================================================
    # SUBJECT / REFRESH
    # =====================================================

    def set_subject(self, subject_id):
        self.current_subject = subject_id
        self.refresh()

    def refresh(self):
        current_task_id = self.current_task_id()

        self.combo.blockSignals(True)
        self.combo.clear()

        if self.task_manager is None or self.current_subject is None:
            self.combo.blockSignals(False)
            return

        tasks = self.task_manager.get_tasks(self.current_subject)
        for task in tasks:
            self.combo.addItem(task["name"], task["id"])

        # Preserve selection where possible
        if current_task_id is not None:
            idx = self.combo.findData(current_task_id)
            if idx >= 0:
                self.combo.setCurrentIndex(idx)

        self.combo.blockSignals(False)

        new_id = self.current_task_id()
        if new_id is not None:
            self.task_changed.emit(new_id)

    # =====================================================
    # TASK ACCESSORS
    # =====================================================

    def current_task_id(self):
        return self.combo.currentData()

    def current_task_name(self):
        return self.combo.currentText()

    # =====================================================
    # ADD / EDIT / DELETE
    # =====================================================

    def add_task(self):
        if self.task_manager is None:
            return
        if self.current_subject is None:
            return

        dialog = AddTaskDialog(
            parent=self,
            default_subject_id=self.current_subject,
        )
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        data = dialog.value()
        if not data:
            return

        self.task_manager.add_task(
            subject_id=data["subject_id"],
            name=data["name"],
            priority=data["priority"],
        )
        # refresh happens automatically via task_changed → refresh

    def edit_task(self):
        if self.task_manager is None:
            return

        task_id = self.current_task_id()
        if task_id is None:
            return

        task = self.task_manager.get_task(task_id)
        if task is None:
            return

        dialog = AddTaskDialog(
            parent=self,
            task=task,
        )
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        data = dialog.value()
        if not data:
            return

        self.task_manager.update_task(
            task_id=task_id,
            name=data["name"],
            subject_id=data["subject_id"],
            priority=data["priority"],
        )
        # refresh happens automatically via task_changed → refresh

    def delete_task(self):
        if self.task_manager is None:
            return

        task_id = self.current_task_id()
        if task_id is None:
            return

        self.task_manager.remove_task(task_id)