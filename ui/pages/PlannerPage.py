from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QDialog,
    QScrollArea, QStackedWidget,
)

from ui.components.MessageBox import ThemedMessageBox

from ui.styles.spacing import SMALL, MEDIUM, LARGE

from ui.styles.styles import (
    menu_label_style,
    selector_label_style,
    Add_btn,
    PLANNER_TASK_ROW,
    PLANNER_TASK_ROW_HOVER,
    PLANNER_EMPTY,
    PLANNER_FILTER_BASE,
    PLANNER_SCROLL_AREA,
    PLANNER_STACK_WRAP,
    PLANNER_CHECKBOX_EMPTY,
    PLANNER_ROW_EDIT_BTN,
    PLANNER_ROW_DELETE_BTN,
    PLANNER_TASK_NAME,
    PLANNER_TASK_NAME_DONE,
    planner_filter_active,
    planner_subject_chip,
    planner_priority_stripe,
    planner_checkbox_done,
)

from assets.icon.icon import ADD, DELETE, EDIT

from managers.TaskManager import TaskManager
from managers.SubjectManager import SubjectManager

from widgets.AddTaskDialog import AddTaskDialog


# ═══════════════════════════════════════════════════════
# Priority tiers
# ═══════════════════════════════════════════════════════
PRIORITIES = [
    {"key": "critical", "label": "Critical", "color": "#EF4444"},
    {"key": "high",     "label": "High",     "color": "#F97316"},
    {"key": "medium",   "label": "Medium",   "color": "#FACC15"},
    {"key": "low",      "label": "Low",      "color": "#22C55E"},
]
PRIORITY_BY_KEY = {p["key"]: p for p in PRIORITIES}


def _dot_pixmap(color, size=14):
    pix = QPixmap(size, size)
    pix.fill(Qt.GlobalColor.transparent)
    p = QPainter(pix)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    p.setBrush(QColor(color))
    p.setPen(Qt.PenStyle.NoPen)
    p.drawEllipse(0, 0, size, size)
    p.end()
    return pix


def _dot_icon(color, size=14):
    return QIcon(_dot_pixmap(color, size))


# ═══════════════════════════════════════════════════════
# Task Row
# ═══════════════════════════════════════════════════════
class TaskRow(QFrame):

    toggled = Signal(int, bool)
    edit_requested = Signal(int)
    delete_requested = Signal(int)

    def __init__(self, task, subject=None, parent=None):
        super().__init__(parent)
        self._task = task
        self._completed = bool(task.get("completed", False))
        self._priority = PRIORITY_BY_KEY.get(
            task.get("priority", "medium"),
            PRIORITY_BY_KEY["medium"],
        )

        self.setObjectName("plannerTaskRow")
        self.setFixedHeight(56)

        outer = QHBoxLayout(self)
        outer.setContentsMargins(0, 0, MEDIUM, 0)
        outer.setSpacing(0)

        stripe = QFrame()
        stripe.setFixedWidth(5)
        stripe.setStyleSheet(
            planner_priority_stripe(self._priority["color"])
        )
        outer.addWidget(stripe)

        wrap = QWidget()
        wrap.setStyleSheet("background: transparent;")
        outer.addWidget(wrap, 1)

        layout = QHBoxLayout(wrap)
        layout.setContentsMargins(MEDIUM, 0, 0, 0)
        layout.setSpacing(MEDIUM)

        self.check_btn = QPushButton()
        self.check_btn.setFixedSize(22, 22)
        self.check_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.check_btn.clicked.connect(self._on_check)
        layout.addWidget(self.check_btn)
        self._refresh_check_style()

        dot = QLabel()
        dot.setPixmap(_dot_pixmap(self._priority["color"], 10))
        dot.setFixedSize(10, 10)
        dot.setToolTip(self._priority["label"])
        layout.addWidget(dot)

        self.name_lbl = QLabel(task.get("name", "(untitled)"))
        self.name_lbl.setStyleSheet(self._name_style())
        layout.addWidget(self.name_lbl, 1)

        if subject:
            chip = QLabel(subject["name"])
            chip.setStyleSheet(
                planner_subject_chip(subject.get("color", "#4F7CFF"))
            )
            layout.addWidget(chip)

        edit_btn = QPushButton()
        edit_btn.setIcon(QIcon(str(EDIT)))
        edit_btn.setIconSize(QSize(15, 15))
        edit_btn.setFixedSize(32, 32)
        edit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        edit_btn.setStyleSheet(PLANNER_ROW_EDIT_BTN)
        edit_btn.setToolTip("Edit task")
        edit_btn.clicked.connect(
            lambda: self.edit_requested.emit(self._task["id"])
        )
        layout.addWidget(edit_btn)

        del_btn = QPushButton()
        del_btn.setIcon(QIcon(str(DELETE)))
        del_btn.setIconSize(QSize(15, 15))
        del_btn.setFixedSize(32, 32)
        del_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        del_btn.setStyleSheet(PLANNER_ROW_DELETE_BTN)
        del_btn.setToolTip("Delete task")
        del_btn.clicked.connect(
            lambda: self.delete_requested.emit(self._task["id"])
        )
        layout.addWidget(del_btn)

        self.setStyleSheet(PLANNER_TASK_ROW)

    def _name_style(self):
        if self._completed:
            return PLANNER_TASK_NAME_DONE
        return PLANNER_TASK_NAME

    def _refresh_check_style(self):
        if self._completed:
            self.check_btn.setText("✓")
            self.check_btn.setStyleSheet(
                planner_checkbox_done(self._priority["color"])
            )
        else:
            self.check_btn.setText("")
            self.check_btn.setStyleSheet(PLANNER_CHECKBOX_EMPTY)

    def _on_check(self):
        self._completed = not self._completed
        self._refresh_check_style()
        self.name_lbl.setStyleSheet(self._name_style())
        self.toggled.emit(self._task["id"], self._completed)

    def enterEvent(self, event):
        self.setStyleSheet(PLANNER_TASK_ROW_HOVER)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setStyleSheet(PLANNER_TASK_ROW)
        super().leaveEvent(event)


# ═══════════════════════════════════════════════════════
# Filter Pill
# ═══════════════════════════════════════════════════════
class FilterPill(QPushButton):

    def __init__(self, key, label, color, count, parent=None):
        super().__init__(parent)
        self.key = key
        self._color = color
        self._count = count
        self._active = False

        self.setFixedHeight(38)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setIcon(_dot_icon(color, 12))
        self.setIconSize(QSize(12, 12))
        self.setStyleSheet(PLANNER_FILTER_BASE)
        self._refresh()

    def update_count(self, count):
        self._count = count
        self._refresh()

    def set_active(self, active):
        self._active = active
        self._refresh()

    def _refresh(self):
        if self.key == "all":
            text = f"All  {self._count}"
        else:
            text = f"{PRIORITY_BY_KEY[self.key]['label']}  {self._count}"
        self.setText("  " + text)

        if self._active:
            self.setStyleSheet(planner_filter_active(self._color))
        else:
            self.setStyleSheet(PLANNER_FILTER_BASE)


# ═══════════════════════════════════════════════════════
# Planner Page
# ═══════════════════════════════════════════════════════
class PlannerPage(QWidget):

    def __init__(self):
        super().__init__()

        self.task_manager = TaskManager()
        self.subject_manager = SubjectManager()

        self.current_filter = None
        self.filter_pills = {}

        self.setup_ui()
        self.connect_signals()

        self.task_manager.task_changed.connect(self.refresh)
        self.subject_manager.subject_changed.connect(self.refresh)
        self.refresh()

    def setup_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(LARGE, LARGE, LARGE, LARGE)
        root.setSpacing(MEDIUM)

        title = QLabel("Planner")
        title.setStyleSheet(menu_label_style)
        root.addWidget(title)

        subtitle = QLabel("Prioritize your tasks by urgency and importance.")
        subtitle.setStyleSheet(selector_label_style)
        root.addWidget(subtitle)

        filter_row = QHBoxLayout()
        filter_row.setSpacing(SMALL)

        all_pill = FilterPill("all", "All", "#4F7CFF", 0)
        all_pill.clicked.connect(lambda: self._on_filter("all"))
        filter_row.addWidget(all_pill)
        self.filter_pills["all"] = all_pill

        for p in PRIORITIES:
            pill = FilterPill(p["key"], p["label"], p["color"], 0)
            pill.clicked.connect(
                lambda checked=False, k=p["key"]: self._on_filter(k)
            )
            filter_row.addWidget(pill)
            self.filter_pills[p["key"]] = pill

        filter_row.addStretch()

        self.add_button = QPushButton("  Add Task")
        self.add_button.setIcon(QIcon(str(ADD)))
        self.add_button.setIconSize(QSize(20, 20))
        self.add_button.setFixedHeight(48)
        self.add_button.setMinimumWidth(180)
        self.add_button.setStyleSheet(Add_btn)
        self.add_button.setCursor(Qt.CursorShape.PointingHandCursor)
        filter_row.addWidget(self.add_button)

        root.addLayout(filter_row)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll.setStyleSheet(PLANNER_SCROLL_AREA)

        self.list_container = QWidget()
        self.list_layout = QVBoxLayout(self.list_container)
        self.list_layout.setContentsMargins(0, 0, 0, 0)
        self.list_layout.setSpacing(SMALL)
        self.list_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll.setWidget(self.list_container)

        empty_wrap = QWidget()
        empty_wrap.setStyleSheet(PLANNER_STACK_WRAP)
        empty_layout = QVBoxLayout(empty_wrap)
        empty_layout.setContentsMargins(0, 0, 0, 0)

        self.empty_label = QLabel("No tasks yet.")
        self.empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.empty_label.setStyleSheet(PLANNER_EMPTY)

        empty_layout.addStretch()
        empty_layout.addWidget(self.empty_label)
        empty_layout.addStretch()

        self.stack = QStackedWidget()
        self.stack.addWidget(self.scroll)
        self.stack.addWidget(empty_wrap)

        root.addWidget(self.stack, 1)

        self._update_filter_visual()

    def connect_signals(self):
        self.add_button.clicked.connect(self.add_task)

    def _on_filter(self, key):
        self.current_filter = None if key == "all" else key
        self._update_filter_visual()
        self.refresh()

    def _update_filter_visual(self):
        for key, pill in self.filter_pills.items():
            if key == "all":
                pill.set_active(self.current_filter is None)
            else:
                pill.set_active(self.current_filter == key)

    def refresh(self):
        self.filter_pills["all"].update_count(
            self.task_manager.count_by_priority(None)
        )
        for p in PRIORITIES:
            self.filter_pills[p["key"]].update_count(
                self.task_manager.count_by_priority(p["key"])
            )

        tasks = self.task_manager.get_tasks_by_priority(self.current_filter)

        while self.list_layout.count():
            item = self.list_layout.takeAt(0)
            w = item.widget()
            if w is not None:
                w.deleteLater()

        if not tasks:
            if self.current_filter is None:
                self.empty_label.setText(
                    "No tasks yet — click + Add Task to get started."
                )
            else:
                label = PRIORITY_BY_KEY[self.current_filter]["label"]
                self.empty_label.setText(f"No “{label}” tasks.")
            self.stack.setCurrentIndex(1)
            return

        self.stack.setCurrentIndex(0)

        subjects = {s["id"]: s for s in self.subject_manager.get_subjects()}

        for task in tasks:
            subject = subjects.get(task.get("subject_id"))
            row = TaskRow(task, subject=subject)
            row.toggled.connect(self._on_toggled)
            row.edit_requested.connect(self.edit_task)
            row.delete_requested.connect(self.delete_task)
            self.list_layout.addWidget(row)

    def _on_toggled(self, task_id, completed):
        self.task_manager.set_completed(task_id, completed)

    def add_task(self):
        subjects = self.subject_manager.get_subjects()
        if not subjects:
            ThemedMessageBox.info(
                self,
                "No subjects yet",
                "Add a subject first (Timer → Session Setup → Subject).",
            )
            return

        default_priority = (
            self.current_filter if self.current_filter is not None else "medium"
        )
        dialog = AddTaskDialog(
            parent=self,
            default_priority=default_priority,
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

    def edit_task(self, task_id):
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

    def delete_task(self, task_id):
        task = self.task_manager.get_task(task_id)
        if task is None:
            return
        if not ThemedMessageBox.confirm_danger(
            self,
            "Delete Task",
            f"Delete “{task.get('name', 'this task')}”?\n\nThis cannot be undone.",
            "Delete",
        ):
            return
        self.task_manager.remove_task(task_id)