from PySide6.QtWidgets import QWidget , QVBoxLayout
from ui.components.card import Card
from widgets.clock import ClockWidget

class  Clockpage(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout()
        self.clock = ClockWidget()
        self.clock_card = Card()
        self.clock_card.add_widget(self.clock)
        main_layout.addWidget(self.clock_card)
        self.setLayout(main_layout)
