#انواع حرکت انیمیشن

from PySide6.QtCore import QEasingCurve


SMOOTH = QEasingCurve.Type.OutCubic

SPRING = QEasingCurve.Type.OutBack #فنری

FAST = QEasingCurve.Type.OutQuad

FADE = QEasingCurve.Type.InOutQuad
