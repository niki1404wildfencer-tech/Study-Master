from ui.styles.fonts import *
from ui.styles.colors import *
from ui.styles.radius import *


SCROLLBAR_STYLE = f"""
QScrollBar:vertical {{
    background: #F0F2F5;
    width: 10px;
    border-radius: 5px;
    margin: 2px 0;
    border: none;
}}
QScrollBar::handle:vertical {{
    background: {TEXT_SECONDARY};
    border-radius: 4px;
    min-height: 36px;
    margin: 2px 2px;
}}
QScrollBar::handle:vertical:hover {{
    background: {TEXT};
}}
QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {{
    height: 0;
    background: transparent;
}}
QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical {{
    background: transparent;
}}

QScrollBar:horizontal {{
    background: #F0F2F5;
    height: 10px;
    border-radius: 5px;
    margin: 0 2px;
    border: none;
}}
QScrollBar::handle:horizontal {{
    background: {TEXT_SECONDARY};
    border-radius: 4px;
    min-width: 36px;
    margin: 2px 2px;
}}
QScrollBar::handle:horizontal:hover {{
    background: {TEXT};
}}
QScrollBar::add-line:horizontal,
QScrollBar::sub-line:horizontal {{
    width: 0;
    background: transparent;
}}
QScrollBar::add-page:horizontal,
QScrollBar::sub-page:horizontal {{
    background: transparent;
}}
"""


main_window_style = f"""
QWidget {{
    background: {BACKGROUND};
    color: {TEXT};
}}
{SCROLLBAR_STYLE}
"""

card_style = f"""
QFrame{{

    background:{CARD};

    border:1px solid {BORDER};

    border-radius:{CARD}px;

}}
"""

card_hover_style = f"""
    QFrame{{

    background:{CARD_HOVER};

    border:1px solid {PRIMARY};

    border-radius:{CARD}px;

}}

"""
button_style =  f"""
QPushButton{{

    background-color:{PRIMARY_btn};

    color:{TEXT_LIGHT};

    border:1px solid rgba(255,255,255,30);

    border-radius:{BUTTON}px;

    padding:14px 22px;

    font-family:{FONT_STACK};

    font-size:{BUTTON_SIZE}px;

    font-weight:600;
}}

QPushButton:hover{{

    background-color:{PRIMARY_HOVER_btn};
    border:1px solid rgba(255,255,255,70);

}}

QPushButton:pressed{{

    background-color:{PRIMARY_PRESSED_btn};

    padding-top:15px;
    padding-bottom:13px;
}}
"""

active_button_style = f"""
QPushButton{{
    background-color: {ACTIVE};
    color: white;
    border: 1px solid rgba(255,255,255,30);
    border-radius: {BUTTON}px;
    padding: 14px 22px;
    font-size: {BUTTON}px;
    font-family: {FONT_STACK};
}}

QPushButton:hover{{
    background-color: {ACTIVE};
}}
"""
menu_label_style =f"""
QLabel{{

    color:{TEXT};

    background:transparent;

    font-size:30px;

    font-weight:bold;

}}
"""
time_label_style = f"""
QLabel{{

    color:{TEXT};

    background:transparent;

}}
"""
ACTIVE_BUTTON_STYLE = f"""
QPushButton{{

    background-color:{SECONDARY};

    color:white;

    border:none;

    border-left:6px solid {PRIMARY};

    border-radius:{BUTTON}px;

    padding:18px;

    font-family:{FONT_STACK};

    font-size:{BUTTON_SIZE}px;

    font-weight:bold;
}}
"""
SIDEBAR_BUTTON_STYLE = f"""
QPushButton {{
    background: transparent;
    border: none;
    border-radius: 14px;
    padding: 18px 22px;
    color: #4B5563;
    font-family: {FONT_STACK};
    font-size: 16px;
    font-weight: 600;
    text-align: left;
}}
QPushButton:hover {{
    background: rgba(79, 124, 255, 0.08);
    color: #4F7CFF;
}}
QPushButton:pressed {{
    background: rgba(79, 124, 255, 0.16);
}}

"""

SIDEBAR_BUTTON_ACTIVE = f"""
QPushButton {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 rgba(79, 124, 255, 0.22),
        stop:1 rgba(50, 212, 198, 0.10));
    border: none;
    border-radius: 14px;
    padding: 22px 24px;
    color: #4F7CFF;
    font-family: {FONT_STACK};
    font-size: 17px;
    font-weight: 800;
    text-align: left;
}}
"""
COMBO_BOX = f"""
QComboBox, QSpinBox {{
    background-color: {CARD};
    color: {TEXT};
    border: 1px solid {BORDER};
    border-radius: 10px;
    padding: 6px 10px;
    font-family: {FONT_STACK};
    font-size: 14px;
    font-weight: 500;
}}

QComboBox:hover, QSpinBox:hover {{
    border: 1px solid {PRIMARY};
}}

QComboBox:focus, QSpinBox:focus {{
    border: 2px solid {PRIMARY};
}}

QComboBox::drop-down {{
    border: none;
    width: 28px;
}}

QComboBox::down-arrow {{
    width: 12px;
    height: 12px;
}}

QSpinBox::up-button,
QSpinBox::down-button {{
    width: 20px;
    border: none;
    background: transparent;
}}

QSpinBox::up-button:hover,
QSpinBox::down-button:hover {{
    background: {CARD_HOVER};
}}
"""
SESSION_BUTTON = f"""
QPushButton {{
    background-color: {SESSION_BUTTON};
    color: {SESSION_TEXT};

    border: none;
    border-radius: {BUTTON_RADIUS}px;

    padding: 16px 24px;

    font-family: {FONT_STACK};
    font-size: {SESSION_BTNSIZE}px;
    font-weight: 700;
}}

QPushButton:hover {{
    background-color: {HOVER_SESSION};
}}

QPushButton:pressed {{
    background-color: {PRIMARY};
}}
"""
selector_label_style = f"""
QLabel {{
    color: {TEXT_SECONDARY};
    background: transparent;
    font-family: {FONT_STACK};
    font-size: 13px;
    font-weight: 600;
}}
"""


input_box = f"""
            QLineEdit {{
                background: {CARD};
                color: {TEXT};
                border: 1px solid {BORDER};
                border-radius: 10px;
                padding: 8px 12px;
                font-family: {FONT_STACK};
                font-size: 14px;
            }}

            QLineEdit:focus {{
                border: 2px solid {PRIMARY};
            }}
        """
search_bar = f"""
QLineEdit {{
    background-color: #ffffff;
    color: #0a0a0a;
    border: 1px solid #d8d8d8;
    border-radius: 14px;
    padding: 8px 16px;
    font-family: {NOTE_FONT_STACK};
    font-size: 18px;
}}

QLineEdit:focus {{
    border: 2px solid #36ccd1;
}}
"""
note_template = f"""
            QFrame {{
                background-color: #ffffff;
                border: 1px solid #e1e1e1;
                border-radius: 18px;
            }}
            """
note_content = f"""
QLabel {{
    font-family: {NOTE_FONT_STACK};
    font-size: 18px;
    color: #555555;
    border: none;
}}
"""

Add_btn =f"""
QPushButton {{
    background-color: {ADD_BACK};
    color: {ADD_TEXT};

    border: none;
    border-radius: {BUTTON_RADIUS}px;

    padding: 16px 24px;

    font-family: {FONT_STACK};
    font-size: {ADD_SIZE}px;
    font-weight: 700;
}}

QPushButton:hover {{
    background-color: {ADD_HOVER};
}}

QPushButton:pressed {{
    background-color: {PRIMARY};
}}
"""
selector = f"""
QComboBox {{
    background-color: {CARD};
    color: {TEXT};

    border: 1px solid {BORDER};
    border-radius: 12px;

    padding: 8px 14px;

    font-family: {FONT_STACK};
    font-size: 16px;
    font-weight: 600;
}}

QComboBox:hover {{
    border: 1px solid {PRIMARY};
    background-color: {CARD_HOVER};
}}

QComboBox:focus {{
    border: 2px solid {PRIMARY};
}}

QComboBox::drop-down {{
    border: none;
    width: 32px;
}}

QComboBox::down-arrow {{
    width: 10px;
    height: 10px;
}}

QComboBox QAbstractItemView {{
    background-color: {CARD};
    color: {TEXT};

    border: 1px solid {BORDER};
    border-radius: 10px;

    padding: 6px;

    selection-background-color: {PRIMARY};
    selection-color: {TEXT_LIGHT};
}}
"""
DAILY_GOAL_PROGRESS = """
QProgressBar {
    background-color: #eeeeee;
    border: none;
    border-radius: 6px;
}

QProgressBar::chunk {
    background-color: #36CCD1;
    border-radius: 6px;
}
"""
# =========================================================
# DIALOGS
# =========================================================

DIALOG_STYLE = f"""
QDialog {{
    background-color: {CARD};
    color: {TEXT};
}}

QDialog QLabel {{
    background: transparent;
    color: {TEXT};
}}

QDialog QLineEdit,
QDialog QTextEdit,
QDialog QComboBox,
QDialog QSpinBox {{
    background-color: {CARD};
    color: {TEXT};
    border: 1px solid {BORDER};
    border-radius: {INPUT_RADIUS}px;
    padding: 10px 14px;
    font-family: {FONT_STACK};
    font-size: 16px;
}}

QDialog QLineEdit:focus,
QDialog QTextEdit:focus,
QDialog QComboBox:focus,
QDialog QSpinBox:focus {{
    border: 2px solid {PRIMARY};
}}

QDialog QPushButton {{
    background-color: {PRIMARY};
    color: {TEXT_LIGHT};
    border: none;
    border-radius: {BUTTON_RADIUS}px;
    padding: 10px 22px;
    min-width: 110px;
    min-height: 44px;
    font-family: {FONT_STACK};
    font-size: 15px;
    font-weight: 600;
}}

QDialog QPushButton:hover {{
    background-color: {PRIMARY_HOVER};
}}

QDialog QPushButton:pressed {{
    background-color: {PRIMARY_PRESSED};
}}

QDialog QPushButton#cancelButton {{
    background-color: {CARD_HOVER};
    color: {TEXT};
    border: 1px solid {BORDER};
}}

QDialog QPushButton#cancelButton:hover {{
    background-color: {BORDER};
}}

QDialog QDialogButtonBox {{
    background: transparent;
}}
"""


MESSAGE_BOX_STYLE = f"""
QDialog {{
    background-color: {CARD};
    border: 1px solid {BORDER};
    border-radius: {CARD_RADIUS}px;
}}

QDialog QLabel {{
    background: transparent;
    color: {TEXT};
}}

QDialog QPushButton {{
    background-color: {PRIMARY};
    color: {TEXT_LIGHT};
    border: none;
    border-radius: {BUTTON_RADIUS}px;
    min-width: 120px;
    min-height: 46px;
    padding: 10px 20px;
    font-family: {FONT_STACK};
    font-size: 16px;
    font-weight: 600;
}}

QDialog QPushButton:hover {{
    background-color: {PRIMARY_HOVER};
}}

QDialog QPushButton:pressed {{
    background-color: {PRIMARY_PRESSED};
}}
"""
selector_shared = f"""
QComboBox, QPushButton {{
    background-color: {CARD};
    color: {TEXT};
    border: 1px solid {BORDER};
    border-radius: 12px;
    padding: 8px 14px;
    font-family: {FONT_STACK};
    font-size: 16px;
    font-weight: 600;
}}

QComboBox:hover, QPushButton:hover {{
    border: 1px solid {PRIMARY};
    background-color: {CARD_HOVER};
}}

QComboBox:focus, QPushButton:focus {{
    border: 2px solid {PRIMARY};
}}

QComboBox::drop-down {{
    border: none;
    width: 32px;
}}

QComboBox::down-arrow {{
    width: 10px;
    height: 10px;
}}

QComboBox QAbstractItemView {{
    background-color: {CARD};
    color: {TEXT};
    border: 1px solid {BORDER};
    border-radius: 10px;
    padding: 6px;
    selection-background-color: {PRIMARY};
    selection-color: {TEXT_LIGHT};
}}
"""
# =========================================================
# CALENDAR
# =========================================================

CALENDAR_TITLE = f"""
QLabel {{
    color: {TEXT};
    background: transparent;
    font-family: {FONT_STACK};
    font-size: 22px;
    font-weight: 800;
}}
"""

CALENDAR_DAY_NAME = f"""
QLabel {{
    color: {TEXT_SECONDARY};
    background: transparent;
    font-family: {FONT_STACK};
    font-size: 13px;
    font-weight: 700;
    padding: 6px 0;
}}
"""

CALENDAR_DAY = f"""
QPushButton {{
    background: transparent;
    border: none;
    border-radius: 8px;
    color: {TEXT};
    font-family: {FONT_STACK};
    font-size: 14px;
    font-weight: 600;
}}
QPushButton:hover {{
    background: rgba(79, 124, 255, 0.10);
}}
"""

CALENDAR_DAY_WEEKEND = f"""
QPushButton {{
    background: transparent;
    border: none;
    border-radius: 8px;
    color: {ERROR};
    font-family: {FONT_STACK};
    font-size: 14px;
    font-weight: 700;
}}
QPushButton:hover {{
    background: rgba(239, 68, 68, 0.10);
}}
"""

CALENDAR_DAY_TODAY = f"""
QPushButton {{
    background: {PRIMARY};
    color: {TEXT_LIGHT};
    border: none;
    border-radius: 8px;
    font-family: {FONT_STACK};
    font-size: 14px;
    font-weight: 800;
}}
"""

CALENDAR_DAY_EMPTY = f"""
QPushButton {{
    background: transparent;
    border: none;
    color: transparent;
}}
"""

CALENDAR_TOGGLE_ACTIVE = f"""
QPushButton {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 rgba(79, 124, 255, 0.22),
        stop:1 rgba(50, 212, 198, 0.10));
    color: {PRIMARY};
    border: 1px solid {PRIMARY};
    border-radius: 12px;
    padding: 8px 14px;
    font-family: {FONT_STACK};
    font-size: 16px;
    font-weight: 800;
}}
"""
# =========================================================
# CALENDAR (day cells + events)
# =========================================================

# =========================================================
# CALENDAR
# =========================================================

CALENDAR_TITLE = f"""
QLabel {{
    color: {TEXT};
    background: transparent;
    font-family: {FONT_STACK};
    font-size: 22px;
    font-weight: 800;
}}
"""

CALENDAR_DAY_NAME = f"""
QLabel {{
    color: {TEXT_SECONDARY};
    background: transparent;
    font-family: {FONT_STACK};
    font-size: 13px;
    font-weight: 700;
    padding: 6px 0;
}}
"""

CALENDAR_DAY_CELL = f"""
QFrame {{
    background: transparent;
    border: none;
    border-radius: 8px;
}}
QFrame:hover {{
    background: rgba(79, 124, 255, 0.10);
}}
"""

CALENDAR_DAY_CELL_TODAY = f"""
QFrame {{
    background: {PRIMARY};
    border: none;
    border-radius: 8px;
}}
"""

CALENDAR_DAY_CELL_WEEKEND = f"""
QFrame {{
    background: rgba(239, 68, 68, 0.10);
    border: none;
    border-radius: 8px;
}}
QFrame:hover {{
    background: rgba(239, 68, 68, 0.18);
}}
"""

CALENDAR_DAY_NUMBER = f"""
QLabel {{
    color: {TEXT};
    background: transparent;
    font-family: {FONT_STACK};
    font-size: 14px;
    font-weight: 700;
}}
"""

CALENDAR_DAY_NUMBER_TODAY = f"""
QLabel {{
    color: {TEXT_LIGHT};
    background: transparent;
    font-family: {FONT_STACK};
    font-size: 14px;
    font-weight: 800;
}}
"""

CALENDAR_DAY_NUMBER_WEEKEND = f"""
QLabel {{
    color: {ERROR};
    background: transparent;
    font-family: {FONT_STACK};
    font-size: 14px;
    font-weight: 700;
}}
"""

CALENDAR_DAY_BADGE = f"""
QLabel {{
    color: {ERROR};
    background: transparent;
    font-family: {FONT_STACK};
    font-size: 9px;
    font-weight: 700;
    padding: 1px 2px;
}}
"""

CALENDAR_EVENT_DOTS = f"""
QLabel {{
    color: {TEXT_SECONDARY};
    background: transparent;
    font-family: {FONT_STACK};
    font-size: 10px;
    font-weight: 600;
}}
"""

CALENDAR_TOGGLE_ACTIVE = f"""
QPushButton {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 rgba(79, 124, 255, 0.22),
        stop:1 rgba(50, 212, 198, 0.10));
    color: {PRIMARY};
    border: 1px solid {PRIMARY};
    border-radius: 12px;
    padding: 8px 14px;
    font-family: {FONT_STACK};
    font-size: 16px;
    font-weight: 800;
}}
"""
SHAMSI_CALENDAR = """
            ShamsiPopupCalendar {
                background: #FFFFFF;
                border: 1px solid #E4E8F0;
                border-radius: 12px;
            }
        """
# =========================================================
# NOTES PAGE
# =========================================================

NOTE_PAGE_TITLE = f"""
QLabel {{
    background: transparent;
    color: #0a0a0a;
    font-family: {NOTE_FONT_STACK};
    font-size: 42px;
    font-weight: 700;
}}
"""

NOTE_TEMPLATE_TITLE = f"""
QLabel {{
    background: transparent;
    color: #0a0a0a;
    font-family: {NOTE_FONT_STACK};
    font-size: 24px;
    font-weight: 700;
}}
"""

NOTE_CARD_TITLE = f"""
QLabel {{
    background: transparent;
    color: #0a0a0a;
    font-family: {NOTE_FONT_STACK};
    font-size: 24px;
    font-weight: 700;
}}
"""

NOTE_DELETE_BUTTON = f"""
QPushButton {{
    background: rgba(255, 90, 90, 20);
    color: #c0392b;
    border: 1px solid rgba(192, 57, 43, 60);
    border-radius: 12px;
    font-family: {NOTE_FONT_STACK};
    font-size: 17px;
    font-weight: 600;
}}
QPushButton:hover {{
    background: rgba(192, 57, 43, 30);
}}
QPushButton:pressed {{
    background: rgba(192, 57, 43, 50);
}}
"""


# =========================================================
# NOTE INPUT DIALOG
# =========================================================

NOTE_DIALOG_HEADER = f"""
QLabel {{
    background: transparent;
    color: #0a0a0a;
    font-family: {NOTE_FONT_STACK};
    font-size: 30px;
    font-weight: 700;
}}
"""

NOTE_FORM_LABEL = f"""
QLabel {{
    background: transparent;
    color: #555555;
    font-family: {FONT_STACK};
    font-size: 13px;
    font-weight: 600;
}}
"""

NOTE_CONTENT_INPUT = f"""
QTextEdit {{
    background: #ffffff;
    color: #0a0a0a;
    border: 1px solid #d8d8d8;
    border-radius: 14px;
    padding: 12px;
    font-family: {NOTE_FONT_STACK};
    font-size: 20px;
}}

QTextEdit:focus {{
    border: 2px solid #36ccd1;
}}
"""
# =========================================================
# EVENT DIALOG
# =========================================================

# =========================================================
# EVENT DIALOG
# =========================================================

EVENT_DIALOG_HEADER = f"""
QLabel {{
    background: transparent;
    color: {TEXT};
    font-family: {FONT_STACK};
    font-size: 22px;
    font-weight: 800;
}}
"""

EVENT_FORM_LABEL = f"""
QLabel {{
    background: transparent;
    color: {TEXT_SECONDARY};
    font-family: {FONT_STACK};
    font-size: 13px;
    font-weight: 600;
}}
"""

EVENT_COLOR_BUTTON = f"""
QPushButton {{
    background: {CARD};
    color: {TEXT};
    border: 1px solid {BORDER};
    border-radius: 10px;
    padding: 6px 14px;
    font-family: {FONT_STACK};
    font-size: 14px;
    font-weight: 600;
    text-align: left;
}}
QPushButton:hover {{
    border: 1px solid {PRIMARY};
    background: {CARD_HOVER};
}}
"""

EVENT_COLLAPSIBLE_BUTTON = f"""
QPushButton {{
    background: {CARD};
    color: {TEXT};
    border: 1px solid {BORDER};
    border-radius: 12px;
    padding: 12px 18px;
    font-family: {FONT_STACK};
    font-size: 15px;
    font-weight: 700;
    text-align: left;
}}
QPushButton:hover {{
    border: 1px solid {PRIMARY};
    background: {CARD_HOVER};
}}
"""

EVENT_REMINDER_CONTAINER = f"""
QFrame {{
    background: rgba(79, 124, 255, 0.04);
    border: 1px solid {BORDER};
    border-radius: 12px;
}}
"""

EVENT_REMINDER_ROW = f"""
QFrame {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: 10px;
}}
"""

EVENT_REMOVE_BUTTON = f"""
QPushButton {{
    background: transparent;
    color: {ERROR};
    border: none;
    border-radius: 6px;
    font-size: 15px;
    font-weight: 700;
}}
QPushButton:hover {{
    background: rgba(239, 68, 68, 0.12);
}}
"""

EVENT_ADD_REMINDER_BUTTON = f"""
QPushButton {{
    background: rgba(79, 124, 255, 0.08);
    color: {PRIMARY};
    border: 1px dashed {PRIMARY};
    border-radius: 10px;
    padding: 10px 18px;
    font-family: {FONT_STACK};
    font-size: 14px;
    font-weight: 700;
}}
QPushButton:hover {{
    background: rgba(79, 124, 255, 0.16);
}}
"""

EVENT_SAVE_BUTTON = f"""
QPushButton {{
    background: {PRIMARY};
    color: {TEXT_LIGHT};
    border: none;
    border-radius: {BUTTON_RADIUS}px;
    padding: 8px 26px;
    min-height: 40px;
    font-family: {FONT_STACK};
    font-size: 15px;
    font-weight: 700;
}}
QPushButton:hover {{
    background: {PRIMARY_HOVER};
}}
QPushButton:pressed {{
    background: {PRIMARY_PRESSED};
}}
"""

EVENT_CANCEL_BUTTON = f"""
QPushButton {{
    background: {CARD_HOVER};
    color: {TEXT};
    border: 1px solid {BORDER};
    border-radius: {BUTTON_RADIUS}px;
    padding: 8px 26px;
    min-height: 40px;
    font-family: {FONT_STACK};
    font-size: 15px;
    font-weight: 600;
}}
QPushButton:hover {{
    background: {BORDER};
}}
"""

EVENT_DELETE_BUTTON = f"""
QPushButton {{
    background: rgba(239, 68, 68, 0.10);
    color: {ERROR};
    border: 1px solid rgba(239, 68, 68, 0.30);
    border-radius: {BUTTON_RADIUS}px;
    padding: 8px 22px;
    min-height: 40px;
    font-family: {FONT_STACK};
    font-size: 15px;
    font-weight: 700;
}}
QPushButton:hover {{
    background: rgba(239, 68, 68, 0.20);
}}
"""

EVENT_VALIDATION_ERROR = f"""
QLineEdit {{
    border: 2px solid {ERROR};
    background: rgba(239, 68, 68, 0.04);
}}
"""


EVENT_SCROLL_AREA = f"""
QScrollArea {{
    background: transparent;
    border: none;
}}
QScrollArea > QWidget > QWidget {{
    background: transparent;
}}
QScrollBar:vertical {{
    background: #F0F2F5;
    width: 10px;
    border-radius: 5px;
    margin: 2px 0;
    border: none;
}}
QScrollBar::handle:vertical {{
    background: {TEXT_SECONDARY};
    border-radius: 4px;
    min-height: 36px;
    margin: 2px 2px;
}}
QScrollBar::handle:vertical:hover {{
    background: {TEXT};
}}
QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {{
    height: 0;
    background: transparent;
}}
QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical {{
    background: transparent;
}}
"""
# =========================================================
# EVENT REMINDER OVERLAY
# =========================================================

EVENT_REMINDER_OVERLAY = f"""
QFrame {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: 14px;
}}
"""

EVENT_REMINDER_EMPTY_LABEL = f"""
QLabel {{
    color: {TEXT_SECONDARY};
    background: transparent;
    font-family: {FONT_STACK};
    font-size: 13px;
    font-weight: 500;
    padding: 24px 0;
}}
"""

#DASHBOARD 
DASHBOARD_PAGE_TITLE = """
            font-family: "Segoe UI", "Vazirmatn";
            font-size: 20px;
            font-weight: 800;
            color: #1F2937;
            background: transparent;
        """
DASHBOARD_DAY_LBL = """
                font-family: "Segoe UI", "Vazirmatn";
                font-size: 13px;
                font-weight: 700;
                color: #4F7CFF;
                background: transparent;
            """
DASHBOARD_NAME_LBL = """
                font-family: "Segoe UI", "Vazirmatn";
                font-size: 14px;
                font-weight: 600;
                color: #1F2937;
                background: transparent;
            """
DASHBOARD_TIME_LBL = """
                    font-family: "Segoe UI", "Vazirmatn";
                    font-size: 13px;
                    color: #6B7280;
                    background: transparent;
                """
DASHBOARD_TODO_LBL = """
            font-family: "Segoe UI", "Vazirmatn";
            font-size: 20px;
            font-weight: 800;
            color: #1F2937;
            background: transparent;
        """
CHECK_BOX = """
                font-size: 18px;
                background: transparent;
            """
DASHBOARD_TODO_NAME = """
                font-family: "Segoe UI", "Vazirmatn";
                font-size: 14px;
                font-weight: 600;
                color: {'#9CA3AF' if completed else '#1F2937'};
                background: transparent;
                text-decoration: {'line-through' if completed else 'none'};
            """
DASHBOARD_DAILYGOAL = """
            font-family: "Segoe UI", "Vazirmatn";
            font-size: 15px;
            font-weight: 700;
            color: #1F2937;
            background: transparent;
        """

DASHBOARD_PROGRESS = """
            QProgressBar {
                background-color: #F0F0F0;
                border: none;
                border-radius: 10px;
            }
            QProgressBar::chunk {
                background-color: #4F7CFF;
                border-radius: 10px;
            }
        """

DASHBOARD_EDIT_DAILYGOAL = """
            QPushButton {
                background: rgba(79, 124, 255, 0.10);
                color: #4F7CFF;
                border: none;
                border-radius: 10px;
                font-size: 18px;
                font-weight: 700;
            }
            QPushButton:hover {
                background: rgba(79, 124, 255, 0.20);
            }
        """
# =========================================================
# MESSAGE BOX (redesigned)
# =========================================================

MESSAGE_BOX_DIALOG = f"""
QDialog {{
    background-color: {CARD};
    border: 1px solid {BORDER};
    border-radius: {CARD_RADIUS}px;
}}
"""

MESSAGE_BOX_TITLE = f"""
QLabel {{
    background: transparent;
    color: {TEXT};
    font-family: {FONT_STACK};
    font-size: 22px;
    font-weight: 800;
}}
"""

MESSAGE_BOX_TEXT = f"""
QLabel {{
    background: transparent;
    color: {TEXT_SECONDARY};
    font-family: {FONT_STACK};
    font-size: 15px;
}}
"""

MESSAGE_BOX_PRIMARY_BTN = f"""
QPushButton {{
    background-color: {PRIMARY};
    color: {TEXT_LIGHT};
    border: none;
    border-radius: {BUTTON_RADIUS}px;
    padding: 12px 32px;
    min-width: 120px;
    min-height: 46px;
    font-family: {FONT_STACK};
    font-size: 15px;
    font-weight: 700;
}}
QPushButton:hover {{
    background-color: {PRIMARY_HOVER};
}}
QPushButton:pressed {{
    background-color: {PRIMARY_PRESSED};
}}
"""

MESSAGE_BOX_DANGER_BTN = f"""
QPushButton {{
    background-color: {ERROR};
    color: {TEXT_LIGHT};
    border: none;
    border-radius: {BUTTON_RADIUS}px;
    padding: 12px 32px;
    min-width: 120px;
    min-height: 46px;
    font-family: {FONT_STACK};
    font-size: 15px;
    font-weight: 700;
}}
QPushButton:hover {{
    background-color: #DC2626;
}}
QPushButton:pressed {{
    background-color: #B91C1C;
}}
"""

MESSAGE_BOX_CANCEL_BTN = f"""
QPushButton {{
    background-color: transparent;
    color: {TEXT_SECONDARY};
    border: 1px solid {BORDER};
    border-radius: {BUTTON_RADIUS}px;
    padding: 12px 32px;
    min-width: 120px;
    min-height: 46px;
    font-family: {FONT_STACK};
    font-size: 15px;
    font-weight: 600;
}}
QPushButton:hover {{
    background-color: {CARD_HOVER};
    border-color: {TEXT_SECONDARY};
    color: {TEXT};
}}
QPushButton:pressed {{
    background-color: {BORDER};
}}
"""
# =========================================================
# NOTES — FOLDER PANEL (with hover)
# =========================================================

FOLDER_PANEL = f"""
QFrame#folderPanel {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: {CARD_RADIUS}px;
}}
QFrame#folderPanel:hover {{
    background: {CARD_HOVER};
    border: 1px solid {PRIMARY};
}}
"""

FOLDER_LIST = f"""
QListWidget {{
    background: transparent;
    border: none;
    outline: none;
    font-family: {FONT_STACK};
    font-size: 14px;
    color: {TEXT};
}}
QListWidget::item {{
    padding: 9px 10px;
    border-radius: 8px;
    margin: 2px 0;
}}
QListWidget::item:hover {{
    background: rgba(79, 124, 255, 0.10);
    color: {PRIMARY};
}}
QListWidget::item:selected {{
    background: rgba(79, 124, 255, 0.16);
    color: {PRIMARY};
    font-weight: 700;
}}
QListWidget::item:selected:hover {{
    background: rgba(79, 124, 255, 0.20);
}}
"""
# =========================================================
# MATCHED DIALOG BUTTON PAIR
# =========================================================

DIALOG_CANCEL_BTN = f"""
QPushButton#dialogCancelBtn {{
    background-color: {CARD};
    color: {TEXT};
    border: 1px solid {BORDER};
    border-radius: {BUTTON_RADIUS}px;
    padding: 16px 24px;
    font-family: {FONT_STACK};
    font-size: {ADD_SIZE}px;
    font-weight: 700;
}}
QPushButton#dialogCancelBtn:hover {{
    background-color: {CARD_HOVER};
    border: 1px solid {PRIMARY};
    color: {PRIMARY};
}}
QPushButton#dialogCancelBtn:pressed {{
    background-color: {BORDER};
}}
"""

# =========================================================
# PLANNER
# =========================================================

PLANNER_TASK_ROW = f"""
QFrame#plannerTaskRow {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: 12px;
}}
"""

PLANNER_TASK_ROW_HOVER = f"""
QFrame#plannerTaskRow {{
    background: {CARD_HOVER};
    border: 1px solid {PRIMARY};
    border-radius: 12px;
}}
"""

PLANNER_EMPTY = f"""
QLabel {{
    color: #9CA3AF;
    background: transparent;
    font-family: {FONT_STACK};
    font-size: 15px;
    padding: 60px 0;
}}
"""

PLANNER_FILTER_BASE = f"""
QPushButton {{
    background: {CARD};
    color: {TEXT_SECONDARY};
    border: 1px solid {BORDER};
    border-radius: 20px;
    padding: 8px 20px;
    font-family: {FONT_STACK};
    font-size: 13px;
    font-weight: 700;
    text-align: center;
}}
QPushButton:hover {{
    border: 1px solid {PRIMARY};
    color: {PRIMARY};
}}
"""
# =========================================================
# PLANNER — additions
# =========================================================
PLANNER_SCROLL_AREA = f"""
QScrollArea {{
    background: transparent;
    border: none;
}}
QScrollArea > QWidget > QWidget {{
    background: transparent;
}}
QScrollBar:vertical {{
    background: #F0F2F5;
    width: 10px;
    border-radius: 5px;
    margin: 2px 0;
    border: none;
}}
QScrollBar::handle:vertical {{
    background: {TEXT_SECONDARY};
    border-radius: 4px;
    min-height: 36px;
    margin: 2px 2px;
}}
QScrollBar::handle:vertical:hover {{
    background: {TEXT};
}}
QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {{
    height: 0;
    background: transparent;
}}
QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical {{
    background: transparent;
}}
"""

PLANNER_STACK_WRAP = """
QWidget {
    background: transparent;
}
"""

PLANNER_CHECKBOX_EMPTY = f"""
QPushButton {{
    background: transparent;
    border: 2px solid #CBD5E1;
    border-radius: 6px;
}}
QPushButton:hover {{
    border: 2px solid {PRIMARY};
}}
"""

PLANNER_ROW_EDIT_BTN = f"""
QPushButton {{
    background: transparent;
    border: 1px solid transparent;
    border-radius: 8px;
}}
QPushButton:hover {{
    background: rgba(79, 124, 255, 0.12);
}}
"""

PLANNER_ROW_DELETE_BTN = f"""
QPushButton {{
    background: transparent;
    border: 1px solid transparent;
    border-radius: 8px;
}}
QPushButton:hover {{
    background: rgba(239, 68, 68, 0.12);
}}
"""

PLANNER_TASK_NAME = f"""
QLabel {{
    background: transparent;
    color: {TEXT};
    font-family: {FONT_STACK};
    font-size: 15px;
    font-weight: 600;
}}
"""

PLANNER_TASK_NAME_DONE = f"""
QLabel {{
    background: transparent;
    color: #9CA3AF;
    font-family: {FONT_STACK};
    font-size: 15px;
    font-weight: 500;
    text-decoration: line-through;
}}
"""


# ─── color-parameterized helpers ───
def _hex_to_rgb(hex_color):
    h = hex_color.lstrip("#")
    return (
        int(h[0:2], 16),
        int(h[2:4], 16),
        int(h[4:6], 16),
    )


def planner_filter_active(color):
    r, g, b = _hex_to_rgb(color)
    ...
def planner_filter_active(color):
    r, g, b = _hex_to_rgb(color)
    return f"""
QPushButton {{
    background: rgba({r}, {g}, {b}, 0.16);
    color: {color};
    border: 1px solid {color};
    border-radius: 20px;
    padding: 8px 20px;
    font-family: {FONT_STACK};
    font-size: 13px;
    font-weight: 800;
}}
"""


def planner_subject_chip(color):
    r, g, b = _hex_to_rgb(color)
    return f"""
QLabel {{
    background: rgba({r}, {g}, {b}, 0.14);
    color: {color};
    border-radius: 8px;
    padding: 3px 10px;
    font-family: {FONT_STACK};
    font-size: 11px;
    font-weight: 700;
}}
"""


def planner_priority_stripe(color):
    return f"""
QFrame {{
    background: {color};
    border-top-left-radius: 12px;
    border-bottom-left-radius: 12px;
}}
"""


def planner_checkbox_done(color):
    return f"""
QPushButton {{
    background: {color};
    color: white;
    border: none;
    border-radius: 6px;
    font-family: {FONT_STACK};
    font-size: 14px;
    font-weight: 900;
}}
"""

# =========================================================
# DASHBOARD — To-Do card
# =========================================================

DASHBOARD_TODO_ROW = f"""
QFrame#dashTaskRow {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: 10px;
}}
"""

DASHBOARD_TODO_ROW_HOVER = f"""
QFrame#dashTaskRow {{
    background: {CARD_HOVER};
    border: 1px solid {PRIMARY};
    border-radius: 10px;
}}
"""

DASHBOARD_TODO_TASK_NAME = f"""
QLabel {{
    background: transparent;
    color: {TEXT};
    font-family: {FONT_STACK};
    font-size: 13px;
    font-weight: 600;
}}
"""

DASHBOARD_TODO_TASK_NAME_DONE = f"""
QLabel {{
    background: transparent;
    color: #9CA3AF;
    font-family: {FONT_STACK};
    font-size: 13px;
    font-weight: 500;
    text-decoration: line-through;
}}
"""

DASHBOARD_TODO_VIEW_ALL = f"""
QPushButton {{
    background: transparent;
    color: {PRIMARY};
    border: none;
    border-radius: 6px;
    padding: 4px 10px;
    font-family: {FONT_STACK};
    font-size: 12px;
    font-weight: 700;
}}
QPushButton:hover {{
    background: rgba(79, 124, 255, 0.10);
}}
"""

DASHBOARD_TODO_CHECKBOX_EMPTY = f"""
QPushButton {{
    background: transparent;
    border: 2px solid #CBD5E1;
    border-radius: 5px;
}}
QPushButton:hover {{
    border: 2px solid {PRIMARY};
}}
"""

DASHBOARD_TODO_EMPTY = f"""
QLabel {{
    color: #9CA3AF;
    background: transparent;
    font-family: {FONT_STACK};
    font-size: 13px;
    padding: 40px 0;
}}
"""


def dashboard_todo_checkbox_done(color):
    return f"""
QPushButton {{
    background: {color};
    color: white;
    border: none;
    border-radius: 5px;
    font-family: {FONT_STACK};
    font-size: 12px;
    font-weight: 900;
}}
"""


def dashboard_todo_stripe(color):
    return f"""
QFrame {{
    background: {color};
    border-top-left-radius: 10px;
    border-bottom-left-radius: 10px;
}}
"""


def dashboard_subject_chip(color):
    r, g, b = _hex_to_rgb(color)
    return f"""
QLabel {{
    background: rgba({r}, {g}, {b}, 0.14);
    color: {color};
    border-radius: 6px;
    padding: 2px 8px;
    font-family: {FONT_STACK};
    font-size: 11px;
    font-weight: 700;
}}
"""
# =========================================================
# DASHBOARD — Daily Goal Bar (with hover)
# =========================================================

DASHBOARD_GOAL_BAR = f"""
QFrame#dashGoalBar {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: {CARD}px;
}}
QFrame#dashGoalBar:hover {{
    background: {CARD_HOVER};
    border: 1px solid {PRIMARY};
    border-radius: {CARD}px;
}}
"""
# =========================================================
# ABOUT PAGE — navigation + section styles
# =========================================================

ABOUT_NAV_CARD = f"""
QFrame#aboutNavCard {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: {CARD_RADIUS}px;
}}
QFrame#aboutNavCard:hover {{
    background: {CARD_HOVER};
    border: 1px solid {PRIMARY};
    border-radius: {CARD_RADIUS}px;
}}
"""

ABOUT_NAV_NUM = f"""
QLabel {{
    background: rgba(79, 124, 255, 0.12);
    color: {PRIMARY};
    border-radius: 16px;
    font-family: {FONT_STACK};
    font-size: 16px;
    font-weight: 900;
}}
"""

ABOUT_NAV_TITLE = f"""
QLabel {{
    background: transparent;
    color: {TEXT};
    font-family: {FONT_STACK};
    font-size: 16px;
    font-weight: 800;
}}
"""

ABOUT_NAV_DESC = f"""
QLabel {{
    background: transparent;
    color: {TEXT_SECONDARY};
    font-family: {FONT_STACK};
    font-size: 12px;
}}
"""

ABOUT_SECTION_HEADING = f"""
QLabel {{
    background: transparent;
    color: {TEXT};
    font-family: {FONT_STACK};
    font-size: 22px;
    font-weight: 800;
}}
"""

ABOUT_BODY = f"""
QLabel {{
    background: transparent;
    color: {TEXT};
    font-family: {FONT_STACK};
    font-size: 14px;
}}
"""

ABOUT_BODY_MUTED = f"""
QLabel {{
    background: transparent;
    color: {TEXT_SECONDARY};
    font-family: {FONT_STACK};
    font-size: 13px;
}}
"""

ABOUT_BULLET = f"""
QLabel {{
    background: transparent;
    color: {TEXT};
    font-family: {FONT_STACK};
    font-size: 13px;
}}
"""

ABOUT_STEP_NUM = f"""
QLabel {{
    background: {PRIMARY};
    color: white;
    border-radius: 14px;
    font-family: {FONT_STACK};
    font-size: 13px;
    font-weight: 900;
}}
"""

ABOUT_IMAGE_PLACEHOLDER = f"""
QLabel {{
    background: #F0F2F5;
    color: #9CA3AF;
    border: 2px dashed #CBD5E1;
    border-radius: 12px;
    font-family: {FONT_STACK};
    font-size: 12px;
    font-weight: 600;
}}
"""
ABOUT_VERSION = f"""
QLabel {{
    background: transparent;
    color: {PRIMARY};
    font-family: {FONT_STACK};
    font-size: 14px;
    font-weight: 700;
    letter-spacing: 1px;
}}
"""
ABOUT_TAGLINE = f"""
QLabel {{
    background: transparent;
    color: {TEXT_SECONDARY};
    font-family: {FONT_STACK};
    font-size: 15px;
}}
"""

ABOUT_NAV_CARD = f"""
QFrame#aboutNavCard {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: {CARD_RADIUS}px;
}}
QFrame#aboutNavCard:hover {{
    background: {CARD_HOVER};
    border: 1px solid {PRIMARY};
    border-radius: {CARD_RADIUS}px;
}}
"""

ABOUT_NAV_NUM = f"""
QLabel {{
    background: rgba(79, 124, 255, 0.12);
    color: {PRIMARY};
    border-radius: 16px;
    font-family: {FONT_STACK};
    font-size: 16px;
    font-weight: 900;
}}
"""

ABOUT_NAV_TITLE = f"""
QLabel {{
    background: transparent;
    color: {TEXT};
    font-family: {FONT_STACK};
    font-size: 16px;
    font-weight: 800;
}}
"""

ABOUT_NAV_DESC = f"""
QLabel {{
    background: transparent;
    color: {TEXT_SECONDARY};
    font-family: {FONT_STACK};
    font-size: 12px;
}}
"""

ABOUT_SECTION_HEADING = f"""
QLabel {{
    background: transparent;
    color: {TEXT};
    font-family: {FONT_STACK};
    font-size: 22px;
    font-weight: 800;
}}
"""

ABOUT_BODY = f"""
QLabel {{
    background: transparent;
    color: {TEXT};
    font-family: {FONT_STACK};
    font-size: 14px;
}}
"""

ABOUT_BODY_MUTED = f"""
QLabel {{
    background: transparent;
    color: {TEXT_SECONDARY};
    font-family: {FONT_STACK};
    font-size: 13px;
}}
"""

ABOUT_BULLET = f"""
QLabel {{
    background: transparent;
    color: {TEXT};
    font-family: {FONT_STACK};
    font-size: 13px;
}}
"""

ABOUT_STEP_NUM = f"""
QLabel {{
    background: {PRIMARY};
    color: white;
    border-radius: 14px;
    font-family: {FONT_STACK};
    font-size: 13px;
    font-weight: 900;
}}
"""

ABOUT_IMAGE_PLACEHOLDER = f"""
QLabel {{
    background: #F0F2F5;
    color: #9CA3AF;
    border: 2px dashed #CBD5E1;
    border-radius: 12px;
    font-family: {FONT_STACK};
    font-size: 12px;
    font-weight: 600;
}}
"""

ABOUT_FOOTER = f"""
QLabel {{
    background: transparent;
    color: #9CA3AF;
    font-family: {FONT_STACK};
    font-size: 12px;
}}
"""