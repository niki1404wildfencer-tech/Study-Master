from PySide6.QtCore import Qt, Signal , QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QComboBox,
    QHBoxLayout,
    QPushButton,
    QDialog,
)

from ui.styles.styles import (
    COMBO_BOX,
    selector_label_style,
    Add_btn,
)
from assets.icon.icon import ADD
from widgets.timer.selectors.AddInput import AddInput
from ui.components.MessageBox import ThemedMessageBox

class SubjectSelector(QWidget):

    subject_changed = Signal(int)

    def __init__(self):
        super().__init__()

        self.subject_manager = None

        self.setup_ui()
        self.connect_signals()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0 , 0 , 0 , 0 )
        layout.setSpacing(5)

        self.title = QLabel("Subject")
        self.title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.title.setStyleSheet(selector_label_style)

        self.combo = QComboBox()
        self.combo.setStyleSheet(COMBO_BOX)
        self.combo.setMinimumHeight(42)

        self.add_btn = QPushButton("Add")
        self.add_btn.setStyleSheet(Add_btn)
        self.add_btn.setIcon(QIcon(str(ADD)))
        self.add_btn.setIconSize(QSize(40 , 40))
        self.add_btn.setFixedSize(140, 52)
        self.edit_btn = QPushButton("Edit")
        self.delete_btn = QPushButton("Delete")
        self.edit_btn.setStyleSheet(Add_btn)
        self.delete_btn.setStyleSheet(Add_btn)
        self.edit_btn.setFixedSize(100, 52)
        self.delete_btn.setFixedSize(120, 52)
   
        row = QHBoxLayout()
        row.setContentsMargins(0 ,0 , 0 , 0 )
        row.setSpacing(8)
        row.addWidget(self.combo)
        row.addWidget(self.add_btn)
        row.addWidget(self.edit_btn)
        row.addWidget(self.delete_btn)

        layout.addWidget(self.title)
        layout.addLayout(row)
        self.setLayout(layout)

    def connect_signals(self):

        self.combo.currentIndexChanged.connect(
        self._on_subject_changed
        )

        self.add_btn.clicked.connect(
            self.add_subject
        )
        self.edit_btn.clicked.connect(
            self.edit_subject
        )
        self.delete_btn.clicked.connect(
            self.delete_subject
        )

    def set_subjects(self, subjects):

        self.combo.clear()

        for subject in subjects:

            self.combo.addItem(
                subject["name"],
                subject["id"]
            )
    
    def current_subject_id(self):

        return self.combo.currentData()

    def current_subject_name(self):

        return self.combo.currentText()

    def set_manager(self, manager):

        self.subject_manager = manager

        self.refresh()

    def refresh(self):

        if self.subject_manager is None:
            return

        subjects = (
            self.subject_manager.get_subjects()
        )

        self.set_subjects(
            subjects
        )

    def add_subject(self):

        dialog = AddInput(
            "Add Subject",
            "Enter subject name...",
            self
        )

        if (
            dialog.exec()
            != QDialog.DialogCode.Accepted
        ):
            return

        name , color = dialog.value()

        if not name:
            return

        if self.subject_manager is None:
            return

        self.subject_manager.add_subject(
            name , 
            color
        )

        self.refresh()
        ThemedMessageBox.success(self,"Success" , "Subject added successfully!")
        self.combo.setCurrentIndex(
            self.combo.count() - 1
        )
        
    def edit_subject(self):

        if self.subject_manager is None:
            return

        subject_id = self.current_subject_id()
        if subject_id is None:
            return

        subject = self.subject_manager.get_subject(
            subject_id
            )

        if subject is None:
            return

        dialog = AddInput(
             "Edit Subject","Enter subject name...",self,name=subject["name"],color=subject["color"],)

        if (
                dialog.exec()
            != QDialog.DialogCode.Accepted
        ):
             return

        name, color = dialog.value()

        if not name:
          return

        self.subject_manager.update_subject(
        subject_id,
        name,
        color,
        )

        self.refresh()  
    def delete_subject(self) :
        if self.subject_manager is None : 
            return 
        subject_id = self.current_subject_id()
        if subject_id is None :
            return
        self.subject_manager.remove_subject(
            subject_id
        )        
        self.refresh()
    def _on_subject_changed(self, index):

        subject_id = self.current_subject_id()

        if subject_id is None:
            return

        self.subject_changed.emit(
            subject_id
            )    