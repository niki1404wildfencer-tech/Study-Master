from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QFrame, QGraphicsDropShadowEffect
)
from PySide6.QtGui import QIcon, QColor, QFont, QLinearGradient, QPainter, QPen
from PySide6.QtCore import (
    QSize, Qt, QPoint, QPropertyAnimation, QEasingCurve
)

from assets.icon.icon import *
from ui.styles.Typography import HEAD_FONT
from ui.styles.spacing import *
from ui.styles.styles import menu_label_style


# =====================================================
# استایل سایدبار
# =====================================================

SIDEBAR_CARD_STYLE = """
QFrame#sidebarCard {
    background-color: #FFFFFF;
    border: 1px solid #EDF0F7;
    border-radius: 24px;
}
"""

SIDEBAR_BTN = """
QPushButton {
    background: transparent;
    border: none;
    border-radius: 14px;
    padding: 14px 18px;
    color: #4B5563;
    font-family: "Segoe UI";
    font-size: 15px;
    font-weight: 600;
    text-align: left;
}
QPushButton:hover {
    background: rgba(79, 124, 255, 0.08);
    color: #4F7CFF;
}
QPushButton:pressed {
    background: rgba(79, 124, 255, 0.16);
}
"""

SIDEBAR_BTN_ACTIVE = """
QPushButton {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 rgba(79, 124, 255, 0.20),
        stop:1 rgba(50, 212, 198, 0.10));
    border: none;
    border-radius: 14px;
    padding: 18px 20px;
    color: #4F7CFF;
    font-family: "Segoe UI";
    font-size: 16px;
    font-weight: 800;
    text-align: left;
}
"""

INDICATOR_STYLE = """
QFrame {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #4F7CFF,
        stop:1 #32D4C6);
    border-radius: 3px;
}
"""


# =====================================================
# لیبل با متن گرادیان (Study Master)
# =====================================================

class GradientLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self._colors = ("#4F7CFF", "#32D4C6")
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def set_colors(self, c1, c2):
        self._colors = (c1, c2)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        try :
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)

            # گرادیان افقی برای متن
            grad = QLinearGradient(0, 0, self.width(), 0)
            grad.setColorAt(0.0, QColor(self._colors[0]))
            grad.setColorAt(1.0, QColor(self._colors[1]))
            painter.setPen(QPen(grad , 1))

        
            font = self.font()
            font.setBold(True)
            font.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, 2.0)
            painter.setFont(font)

            painter.drawText(
                self.rect(),
                Qt.AlignmentFlag.AlignCenter,
                self.text()
            )

        finally :
            painter.end()



class Sidebar(QWidget):

    def __init__(self):
        super().__init__()
        self.setFixedWidth(320)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet("background: transparent;")

        self._active_button = None
        self._indicator_anim_pos = None
        self._indicator_anim_size = None
        self._indicator_initialized = False

        self.setup_ui()

    # =====================================================
    # UI
    # =====================================================

    def setup_ui(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(14, 14, 10, 14)
        outer.setSpacing(0)

        # کارت اصلی
        self.card = QFrame()
        self.card.setObjectName("sidebarCard")
        self.card.setStyleSheet(SIDEBAR_CARD_STYLE)

        # شادوی قوی
        shadow = QGraphicsDropShadowEffect(self.card)
        shadow.setBlurRadius(60)
        shadow.setColor(QColor(79, 124, 255, 70))
        shadow.setOffset(0, 10)
        self.card.setGraphicsEffect(shadow)

        inner = QVBoxLayout(self.card)
        inner.setContentsMargins(16, 22, 16, 22)
        inner.setSpacing(6)

        outer.addWidget(self.card)

        # ─── هدر گرادیانی ───
        header_font = QFont("Segoe UI", 22, QFont.Weight.Black)
        self.header = GradientLabel("STUDY MASTER")
        self.header.setFont(header_font)
        self.header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.header.setFixedHeight(46)
        inner.addWidget(self.header)

        # خط جداکننده زیر هدر
        divider = QFrame()
        divider.setFixedHeight(2)
        divider.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(79, 124, 255, 0),
                    stop:0.5 rgba(79, 124, 255, 0.5),
                    stop:1 rgba(50, 212, 198, 0));
                border-radius: 1px;
            }
        """)
        inner.addSpacing(4)
        inner.addWidget(divider)
        inner.addSpacing(14)

        # ─── دکمهها ───
        self.dashboard_btn    = self._make_button("Dashboard", DASHBOARD_ICON)
        self.clock_btn        = self._make_button("Clock",     CLOCK_ICON)
        self.timer_btn        = self._make_button("Timer",     TIMER_ICON)
        self.stopwatch_btn    = self._make_button("Stopwatch", STOPWATCH_ICON)
        self.notes_btn        = self._make_button("Notes",     NOTES_ICON)
        self.planner_btn      = self._make_button("Planner",   PLANNER_ICON)
        self.calendar_btn     = self._make_button("Calendar",  CALENDAR_ICON)
        self.Statistics_btn   = self._make_button("Statistics", STATISTICS_ICON)
        self.about_btn        = self._make_button("About",    ABOUT)

        self.sidebar_btns = [
            self.dashboard_btn, self.clock_btn, self.timer_btn,
            self.stopwatch_btn, self.notes_btn, self.planner_btn,
            self.calendar_btn, self.Statistics_btn,
            self.about_btn,
        ]

        for b in self.sidebar_btns:
            b.setStyleSheet(SIDEBAR_BTN)
            b.setCursor(Qt.CursorShape.PointingHandCursor)

        # ─── چیدمان ───
        top_group = [
            self.dashboard_btn, self.clock_btn,
            self.timer_btn, self.stopwatch_btn,
        ]
        mid_group = [
            self.notes_btn, self.planner_btn,
            self.calendar_btn, self.Statistics_btn,
        ]
        bottom_group = [
            self.about_btn,
        ]

        for b in top_group:
            inner.addWidget(b)

        inner.addSpacing(LARGE)

        for b in mid_group:
            inner.addWidget(b)

        inner.addStretch()

        for b in bottom_group:
            inner.addWidget(b)

        # ─── نشانگر اسلایدی ───
        self.indicator = QFrame(self.card)
        self.indicator.setStyleSheet(INDICATOR_STYLE)
        self.indicator.setFixedWidth(4)
        self.indicator.hide()

        # اتصال دکمهها
        for b in self.sidebar_btns:
            b.clicked.connect(
                lambda checked=False, btn=b: self.set_active_button(btn)
            )

        # دکمه پیشفرض: داشبورد (بدون انیمیشن اولیه)
        self._set_initial_active(self.dashboard_btn)

    # =====================================================
    # ساخت دکمه
    # =====================================================

    def _make_button(self, text, icon_path):
        btn = QPushButton(text)
        if icon_path is not None:
            btn.setIcon(QIcon(str(icon_path)))
            btn.setIconSize(QSize(22, 22))
        return btn

    # =====================================================
    # تنظیم اولیه (بدون انیمیشن)
    # =====================================================

    def _set_initial_active(self, button):
        for b in self.sidebar_btns:
            b.setStyleSheet(SIDEBAR_BTN)

        button.setStyleSheet(SIDEBAR_BTN_ACTIVE)
        self._active_button = button

        # Defer until Qt has computed the layout — otherwise mapTo() returns 0
        from PySide6.QtCore import QTimer
        QTimer.singleShot(100, lambda: self._position_indicator(button))

    def _position_indicator(self, button):
        if button is None:
            return
        try:
            pos_in_card = button.mapTo(self.card, QPoint(0, 0))
        except RuntimeError:
            return
        self.indicator.setGeometry(10, pos_in_card.y(), 4, button.height())
        self.indicator.show()
        self.indicator.raise_()
        self._indicator_initialized = True

    # =====================================================
    # کلیک روی دکمه با انیمیشن
    # =====================================================

    def set_active_button(self, button, animate=True):
        if button is None:
            return

        # اگر همون دکمه فعلیه، کاری نکن
        if button is self._active_button:
            return

        # ریست بقیه
        for b in self.sidebar_btns:
            b.setStyleSheet(SIDEBAR_BTN)

        button.setStyleSheet(SIDEBAR_BTN_ACTIVE)
        self._active_button = button

        # موقعیت جدید نشانگر
        pos_in_card = button.mapTo(self.card, QPoint(0, 0))
        target_x = 10
        target_y = pos_in_card.y()
        target_h = button.height()

        # اگر اولین باره، فقط بذار سر جاش
        if not self._indicator_initialized:
            self.indicator.setGeometry(target_x, target_y, 4, target_h)
            self.indicator.show()
            self.indicator.raise_()
            self._indicator_initialized = True
            return

        # ─── انیمیشن موقعیت ───
        current_pos = self.indicator.pos()
        start_pos = QPoint(current_pos.x(), current_pos.y())
        end_pos = QPoint(target_x, target_y)

        self._indicator_anim_pos = QPropertyAnimation(self.indicator, b"pos")
        self._indicator_anim_pos.setDuration(280)
        self._indicator_anim_pos.setStartValue(start_pos)
        self._indicator_anim_pos.setEndValue(end_pos)
        self._indicator_anim_pos.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._indicator_anim_pos.start()

        # ─── انیمیشن ارتفاع ───
        start_size = QSize(self.indicator.width(), self.indicator.height())
        end_size = QSize(4, target_h)

        self._indicator_anim_size = QPropertyAnimation(self.indicator, b"size")
        self._indicator_anim_size.setDuration(280)
        self._indicator_anim_size.setStartValue(start_size)
        self._indicator_anim_size.setEndValue(end_size)
        self._indicator_anim_size.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._indicator_anim_size.start()

        self.indicator.show()
        self.indicator.raise_()
    def showEvent(self, event):
        super().showEvent(event)
        if self._active_button is not None and not self._indicator_initialized:
            from PySide6.QtCore import QTimer
            QTimer.singleShot(100, lambda: self._position_indicator(self._active_button))

    def reset_buttons(self):
        for b in self.sidebar_btns:
            b.setStyleSheet(SIDEBAR_BTN)
    def reset_buttons(self):
        for b in self.sidebar_btns:
            b.setStyleSheet(SIDEBAR_BTN)