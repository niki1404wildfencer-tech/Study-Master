from PySide6.QtWidgets import  QFrame,QVBoxLayout , QGraphicsDropShadowEffect
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt , QPropertyAnimation

from ui.animations.easing import SMOOTH
from ui.styles.styles import card_style , card_hover_style
from ui.styles.spacing import *
from ui.styles.effects import *
class Card(QFrame):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.animations= []
    def setup_ui(self):
        self.setStyleSheet(card_style)
        #self.setCursor(Qt.CursorShape.PointingHandCursor) # برای دنیال کردن موس
        self.card_layout = QVBoxLayout(self)
        self.card_layout.setContentsMargins(LARGE , LARGE , LARGE , LARGE)
        self.card_layout.setSpacing(MEDIUM)
        self.setMinimumHeight(CARD_MIN_HEIGHT)


        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(SHADOW_BLUR)
        self.shadow.setXOffset(SHADOW_X_OFFSET)
        self.shadow.setYOffset(SHADOW_Y_OFFSET)
        self.shadow.setColor(QColor(0,0,0,SHADOW_ALPHA))
        #): مقدار قرمز (۰ تا ۲۵۵)
        #G (Green): مقدار سبز (۰ تا ۲۵۵)
        #B (Blue): مقدار آبی (۰ تا ۲۵۵)
        #A (Alpha): میزان شفافیت (۰ تا ۲۵۵)

        self.setGraphicsEffect(self.shadow)

    def add_widget(self ,  widget):
        self.card_layout.addWidget(widget)

    def enterEvent(self , event):
        self.setStyleSheet(card_hover_style)
        super().enterEvent(event)
        self.animate_shadow(45)

    def leaveEvent(self, event):
        self.setStyleSheet(card_style)
        super().leaveEvent(event)
        self.animate_shadow(20)
    def animate_shadow(self , endvalue):
        animation = QPropertyAnimation(self.shadow , b"blurRadius")
        animation.setDuration(180)
        animation.setStartValue(self.shadow.setBlurRadius)
        animation.setEndValue(endvalue)
        animation.setEasingCurve(SMOOTH)

        animation.finished.connect(
             lambda: self.animations.remove(animation)
            )

        self.animations.append(animation)

        animation.start()