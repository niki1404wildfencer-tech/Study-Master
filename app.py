import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont, QIcon

from managers.DashboardManager import Dashboard


def main():
    app = QApplication(sys.argv)

    app_font = QFont()
    app_font.setFamilies(["Segoe UI", "Vazirmatn"])
    app_font.setPointSize(10)
    QApplication.setFont(app_font)

    icon_png = Path(__file__).resolve().parent / "assets" / "app_icon.png"
    icon_ico = Path(__file__).resolve().parent / "assets" / "app_icon.ico"

    icon = QIcon()
    if icon_ico.exists():
        icon.addFile(str(icon_ico))
    if icon_png.exists():
        icon.addFile(str(icon_png))

    if not icon.isNull():
        app.setWindowIcon(icon)

    window = Dashboard()
    if not icon.isNull():
        window.setWindowIcon(icon)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()