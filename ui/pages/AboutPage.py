from pathlib import Path

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QScrollArea,
)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QFont, QPixmap

from ui.components.card import Card
from ui.pages.sidebarPage import GradientLabel
from ui.styles.styles import (
    menu_label_style,
    ABOUT_VERSION,
    ABOUT_TAGLINE,
    ABOUT_FOOTER,
    ABOUT_NAV_CARD,
    ABOUT_NAV_NUM,
    ABOUT_NAV_TITLE,
    ABOUT_NAV_DESC,
    ABOUT_SECTION_HEADING,
    ABOUT_BODY,
    ABOUT_BODY_MUTED,
    ABOUT_BULLET,
    ABOUT_STEP_NUM,
    ABOUT_IMAGE_PLACEHOLDER,
)
from ui.styles.spacing import LARGE, MEDIUM, SMALL


# ═══════════════════════════════════════════════════════
# Metadata
# ═══════════════════════════════════════════════════════
APP_NAME = "STUDY MASTER"
APP_VERSION = "1.0.0"
APP_TAGLINE = "Your all-in-one study companion."


# ═══════════════════════════════════════════════════════
# Guide content — edit this list to change images or text
# ═══════════════════════════════════════════════════════
GUIDE_STEPS = [
    (
        "The Dashboard",
        "Your home base. At a glance you get the live clock, timer, "
        "stopwatch, upcoming events, prioritized to-do list, and today's "
        "study progress toward your daily goal.",
        "step1.png",
    ),
    (
        "The Timer",
        "Your Pomodoro timer. Default 20-minute focus session. "
        "Use Start, Reset, and Skip to control your session.",
        "step2.png",
    ),
    (
        "Session Setup",
        "Click the blue Session Setup bar to open this panel. Choose your "
        "Subject, Task, Duration, Daily Goal, and Completion Sound. "
        "Close it any time with the bar at the top.",
        "step3.png",
    ),
    (
        "Folders in Notes",
        "On the Notes page, create folders to group related notes. "
        "Click New Folder, give it a name, and pick a color — the folder "
        "color becomes the accent stripe on every note inside it.",
        "step4.png",
    ),
    (
        "Add a Note",
        "Click Add Note. Choose a folder, optionally link the note to a "
        "subject and task, then write a title and body. Save it — the "
        "note appears immediately in the current folder.",
        "step5.png",
    ),
    (
        "Click a Note to View It",
        "Click anywhere on a note card (not on the buttons) to open the "
        "full view. From there you can Edit or Close without losing "
        "your place.",
        "step6.png",
    ),
    (
        "Plan Tasks by Priority",
        "On the Planner page, every task is color-coded: red for Critical, "
        "orange for High, yellow for Medium, green for Low. Use the "
        "filter pills at the top to focus on one tier at a time.",
        "step7.png",
    ),
    (
        "Add Events to the Calendar",
        "From the Calendar page click + Add Event. Set a title, pick a "
        "color, choose a date and time, and optionally add reminders "
        "that will fire a popup with a sound.",
        "step8.png",
    ),
    (
        "See Your Progress",
        "The Statistics page shows a bar chart of daily study time and a "
        "pie chart of time per subject. Switch between Weekly, Monthly, "
        "Yearly, and All Time. Export the charts as a PDF with one click.",
        "step9.png",
    ),
    (
        "Browse All Your Events",
        "Click All My Events from the Calendar page to see every event in "
        "one list. Use the filter dropdown to jump between Today, "
        "This Week, This Month, All, and Past.",
        "step10.png",
    ),
]


# ═══════════════════════════════════════════════════════
# Helpers
# ═══════════════════════════════════════════════════════
def _guide_dir():
    """Return the absolute path to assets/guide/."""
    return (
        Path(__file__).resolve().parent.parent.parent
        / "assets" / "guide"
    )


# ═══════════════════════════════════════════════════════
# Clickable navigation card
# ═══════════════════════════════════════════════════════
class AboutNavCard(QFrame):

    def __init__(self, number, title, description, target_id, page):
        super().__init__()
        self._target_id = target_id
        self._page = page

        self.setObjectName("aboutNavCard")
        self.setStyleSheet(ABOUT_NAV_CARD)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedHeight(110)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(MEDIUM, MEDIUM, MEDIUM, MEDIUM)
        layout.setSpacing(MEDIUM)

        num_lbl = QLabel(str(number))
        num_lbl.setFixedSize(32, 32)
        num_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        num_lbl.setStyleSheet(ABOUT_NAV_NUM)
        layout.addWidget(num_lbl, alignment=Qt.AlignmentFlag.AlignTop)

        text_col = QVBoxLayout()
        text_col.setSpacing(4)

        title_lbl = QLabel(title)
        title_lbl.setStyleSheet(ABOUT_NAV_TITLE)
        text_col.addWidget(title_lbl)

        desc_lbl = QLabel(description)
        desc_lbl.setWordWrap(True)
        desc_lbl.setStyleSheet(ABOUT_NAV_DESC)
        text_col.addWidget(desc_lbl)

        layout.addLayout(text_col, 1)

        arrow = QLabel("→")
        arrow.setStyleSheet(ABOUT_NAV_TITLE)
        layout.addWidget(arrow, alignment=Qt.AlignmentFlag.AlignVCenter)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._page.scroll_to(self._target_id)
            event.accept()
            return
        super().mousePressEvent(event)


# ═══════════════════════════════════════════════════════
# About Page
# ═══════════════════════════════════════════════════════
class AboutPage(QWidget):

    def __init__(self):
        super().__init__()
        self._anchors = {}
        self._scroll_anim = None
        self.setup_ui()

    # =====================================================
    def setup_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(LARGE, LARGE, LARGE, LARGE)
        root.setSpacing(MEDIUM)

        title = QLabel("About")
        title.setStyleSheet(menu_label_style)
        root.addWidget(title)

        # Scroll area holding everything
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll.setStyleSheet(
            "QScrollArea { background: transparent; border: none; }"
            "QScrollArea > QWidget > QWidget { background: transparent; }"
        )

        content = QWidget()
        content.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(content)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(MEDIUM)

        layout.addWidget(self._make_hero())
        layout.addLayout(self._make_nav_row())
        layout.addWidget(self._make_intro_section())
        layout.addWidget(self._make_developer_section())
        layout.addWidget(self._make_guide_section())

        footer = QLabel(
            "Made for focused studying  •  © 2026 Study Master"
        )
        footer.setStyleSheet(ABOUT_FOOTER)
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(footer)

        layout.addStretch()

        self.scroll.setWidget(content)
        root.addWidget(self.scroll, 1)

    # =====================================================
    # Smooth scroll
    # =====================================================
    def scroll_to(self, section_id):
        anchor = self._anchors.get(section_id)
        if anchor is None:
            return

        content_widget = self.scroll.widget()
        if content_widget is None:
            return

        # anchor.y() is relative to its parent card.
        # mapTo() gives the y inside the scroll content.
        from PySide6.QtCore import QPoint
        target_y = anchor.mapTo(content_widget, QPoint(0, 0)).y()
        target_y = max(0, target_y - 12)

        bar = self.scroll.verticalScrollBar()

        if self._scroll_anim is not None:
            self._scroll_anim.stop()

        anim = QPropertyAnimation(bar, b"value", self)
        anim.setDuration(420)
        anim.setStartValue(bar.value())
        anim.setEndValue(target_y)
        anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        anim.start()
        self._scroll_anim = anim

    # =====================================================
    # Hero
    # =====================================================
    def _make_hero(self):
        card = Card()
        card.setMinimumHeight(0)
        card.setMaximumHeight(190)

        hero = QVBoxLayout()
        hero.setSpacing(6)
        hero.setAlignment(Qt.AlignmentFlag.AlignCenter)

        logo = GradientLabel(APP_NAME)
        f = QFont("Segoe UI", 36, QFont.Weight.Black)
        f.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, 3.0)
        logo.setFont(f)
        logo.setFixedHeight(64)
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hero.addWidget(logo)

        version = QLabel(f"Version  {APP_VERSION}")
        version.setStyleSheet(ABOUT_VERSION)
        version.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hero.addWidget(version)

        tagline = QLabel(APP_TAGLINE)
        tagline.setStyleSheet(ABOUT_TAGLINE)
        tagline.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hero.addWidget(tagline)

        card.card_layout.addLayout(hero)
        return card

    # =====================================================
    # Navigation row
    # =====================================================
    def _make_nav_row(self):
        row = QHBoxLayout()
        row.setSpacing(MEDIUM)

        row.addWidget(AboutNavCard(
            1, "Introduction",
            "What Study Master is and who it's for.",
            "intro", self,
        ))
        row.addWidget(AboutNavCard(
            2, "About the Developer",
            "Who built this and why.",
            "developer", self,
        ))
        row.addWidget(AboutNavCard(
            3, "How to Use",
            "Step-by-step walkthrough with screenshots.",
            "guide", self,
        ))
        return row

    # =====================================================
    # Section 1
    # =====================================================
    def _make_intro_section(self):
        card = Card()
        card.setMinimumHeight(0)

        header = QLabel("1  •  Introduction")
        header.setStyleSheet(ABOUT_SECTION_HEADING)
        self._anchors["intro"] = header
        card.add_widget(header)

        body = QLabel(
            "Study Master is a desktop app made for students who want one "
            "place to plan, focus, and review their study time. "
            "It combines a Pomodoro timer, a stopwatch, a prioritized "
            "to-do list, subject-based notes, a full calendar with Persian "
            "and Gregorian views, and a statistics dashboard — all in one "
            "clean window."
        )
        body.setWordWrap(True)
        body.setStyleSheet(ABOUT_BODY)
        card.add_widget(body)

        bullets = [
            "Track focused study sessions per subject and task",
            "Set a daily goal and watch your progress fill up live",
            "Organize notes into folders and link them to subjects",
            "Prioritize tasks with four color-coded tiers",
            "See daily, weekly, and monthly study trends at a glance",
        ]
        for b in bullets:
            row = QLabel(f"•  {b}")
            row.setWordWrap(True)
            row.setStyleSheet(ABOUT_BULLET)
            card.add_widget(row)

        return card

    # =====================================================
    # Section 2
    # =====================================================
    def _make_developer_section(self):
        card = Card()
        card.setMinimumHeight(0)

        header = QLabel("2  •  About the Developer")
        header.setStyleSheet(ABOUT_SECTION_HEADING)
        self._anchors["developer"] = header
        card.add_widget(header)

        body = QLabel(
            "Built by a student, for students. Every screen was designed "
            "around one goal: make it easier to sit down, focus, and "
            "actually finish what you started."
        )
        body.setWordWrap(True)
        body.setStyleSheet(ABOUT_BODY)
        card.add_widget(body)

        rows = [
            ("Developer",   "Niki Nasirzadeh"),
            ("Email",       "niki.nasirzadeh1399@gmail.com"),
            ("GitHub",      "github.com"),
            ("Linkedin",     "https://www.linkedin.com/in/niki-nasirzadeh-b967263a0"),
        ]
        for label, value in rows:
            row = QHBoxLayout()

            name_lbl = QLabel(label)
            name_lbl.setFixedWidth(120)
            name_lbl.setStyleSheet(ABOUT_BULLET)

            val_lbl = QLabel(value)
            val_lbl.setStyleSheet(ABOUT_BODY_MUTED)

            row.addWidget(name_lbl)
            row.addWidget(val_lbl, 1)

            card.card_layout.addLayout(row)

        return card

    # =====================================================
    # Section 3 — Guide with screenshots
    # =====================================================
    def _make_guide_section(self):
        card = Card()
        card.setMinimumHeight(0)

        header = QLabel("3  •  How to Use")
        header.setStyleSheet(ABOUT_SECTION_HEADING)
        self._anchors["guide"] = header
        card.add_widget(header)

        sub = QLabel(
            "Follow these ten steps and you'll know your way around "
            "Study Master in minutes."
        )
        sub.setWordWrap(True)
        sub.setStyleSheet(ABOUT_BODY_MUTED)
        card.add_widget(sub)

        guide_dir = _guide_dir()

        for index, (step_title, step_desc, filename) in enumerate(GUIDE_STEPS, start=1):
            # ── Step heading row ──
            row = QHBoxLayout()
            row.setSpacing(MEDIUM)

            num_lbl = QLabel(str(index))
            num_lbl.setFixedSize(28, 28)
            num_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            num_lbl.setStyleSheet(ABOUT_STEP_NUM)
            row.addWidget(num_lbl, alignment=Qt.AlignmentFlag.AlignTop)

            text_col = QVBoxLayout()
            text_col.setSpacing(4)

            t = QLabel(step_title)
            t.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
            t.setStyleSheet(ABOUT_BULLET)
            text_col.addWidget(t)

            d = QLabel(step_desc)
            d.setWordWrap(True)
            d.setStyleSheet(ABOUT_BODY_MUTED)
            text_col.addWidget(d)

            row.addLayout(text_col, 1)
            card.card_layout.addLayout(row)

            # ── Screenshot ──
            img = QLabel()
            img.setAlignment(Qt.AlignmentFlag.AlignCenter)
            img.setMinimumHeight(220)
            img.setStyleSheet("background: transparent; border: none;")

            img_path = guide_dir / filename
            pix = QPixmap(str(img_path))

            if not pix.isNull():
                scaled = pix.scaledToHeight(
                    260,
                    Qt.TransformationMode.SmoothTransformation,
                )
                img.setPixmap(scaled)
                img.setMinimumHeight(scaled.height() + 8)
            else:
                img.setText(f"Missing: assets/guide/{filename}")
                img.setStyleSheet(ABOUT_IMAGE_PLACEHOLDER)
                img.setMinimumHeight(180)

            card.add_widget(img)

        return card