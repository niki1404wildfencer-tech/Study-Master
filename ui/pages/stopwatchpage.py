from PySide6.QtWidgets import QWidget , QVBoxLayout
from ui.components.card import Card
from widgets.stopwatch import Stopwatch

class  stopwatch(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout()
        self.stopwatch = Stopwatch()
        self.stopwatch_card = Card()
        self.stopwatch_card.add_widget(self.stopwatch)
        main_layout.addWidget(self.stopwatch_card)
        self.setLayout(main_layout)