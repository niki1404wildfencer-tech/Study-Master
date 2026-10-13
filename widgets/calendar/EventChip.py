from PySide6.QtWidgets import QWidget, QSizePolicy
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPainter, QColor, QPen


class EventChip(QWidget):
    """Small colored pill with the event title, elided if too long."""

    clicked = Signal(dict)

    def __init__(self, event, parent=None):
        super().__init__(parent)
        self._event_data = event
        self._full_title = str(event.get("title", "") or "")
        self._color = QColor(event.get("color", "#4F7CFF"))
        self._hovered = False

        self.setFixedHeight(18)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setToolTip(self._full_title or "(untitled)")

    def enterEvent(self, event):
        self._hovered = True
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hovered = False
        self.update()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            event.accept()
            self.clicked.emit(self._event_data)
            return
        super().mousePressEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        color = self._color.lighter(115) if self._hovered else self._color
        painter.setBrush(color)
        if self._hovered:
            painter.setPen(QPen(QColor("#FFFFFF"), 1))
        else:
            painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect().adjusted(0, 0, -1, -1), 9, 9)

        painter.setPen(QColor("#FFFFFF"))
        font = painter.font()
        font.setPointSize(14)
        font.setBold(True)
        painter.setFont(font)

        fm = painter.fontMetrics()
        text_rect = self.rect().adjusted(8, 0, -4, 0)
        elided = fm.elidedText(
            self._full_title, Qt.TextElideMode.ElideRight, text_rect.width()
        )
        painter.drawText(
            text_rect,
            Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft,
            elided,
        )
        painter.end()