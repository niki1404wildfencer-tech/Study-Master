from PySide6.QtGui import QFont

from ui.styles.fonts import *


# ─── فونت‌های اصلی ───
HEAD_FONT = QFont(
    FONT_FAMILY, HEAD_SIZE,
    QFont.Weight.Bold
)

TITLE_FONT = QFont(
    FONT_FAMILY, TITLE_SIZE,
    QFont.Weight.Bold
)

SUBTITLE_FONT = QFont(
    FONT_FAMILY, SUBTITLE_SIZE,
    QFont.Weight.DemiBold
)

BODY_FONT = QFont(
    FONT_FAMILY, BODY_SIZE,
)

BUTTON_FONT = QFont(
    FONT_FAMILY, BUTTON_SIZE,
    QFont.Weight.Bold
)

CLOCK_FONT = QFont(
    FONT_FAMILY, CLOCK_SIZE,
    QFont.Weight.Bold
)

TIMER_FONT = QFont(
    FONT_FAMILY, TIMER_SIZE,
    QFont.Weight.Bold
)


# ─── فونت‌های Session با fallback فارسی ───
SESSION_SUB_FONT = QFont()
SESSION_SUB_FONT.setFamilies([SESSION_IC, PERSIAN_FONT])
SESSION_SUB_FONT.setPointSize(SUBTITLE_SIZE)
SESSION_SUB_FONT.setWeight(QFont.Weight.Medium)

SESSION_FONT = QFont()
SESSION_FONT.setFamilies([SESSION_IC, PERSIAN_FONT])
SESSION_FONT.setPointSize(TITLE_SIZE)
SESSION_FONT.setWeight(QFont.Weight.Medium)